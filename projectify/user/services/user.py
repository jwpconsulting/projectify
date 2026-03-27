# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023-2024 JWP Consulting GK
"""User model services in user app."""

import logging
from typing import Optional, Union

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import PermissionDenied
from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import transaction
from django.db.models.fields.files import FileDescriptor
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _

from projectify.lib.types import AuthenticatedHttpRequest
from projectify.user.emails import (
    UserEmailAddressUpdatedEmail,
    UserEmailAddressUpdateEmail,
    UserPasswordChangedEmail,
    UserPasswordSetEmail,
)
from projectify.user.models import PreviousEmailAddress, User
from projectify.user.services.internal import Token, user_check_token

logger = logging.getLogger(__name__)


# No Create, since creating users is complicated


# Update
@transaction.atomic()
def user_update(
    *,
    who: User,
    user: User,
    preferred_name: Optional[str],
    profile_picture: Optional[FileDescriptor],
) -> User:
    """Update a user."""
    if not who == user:
        # TODO localize string
        raise PermissionDenied("User can only update own user")
    user.preferred_name = preferred_name
    if profile_picture:
        user.profile_picture = profile_picture
    user.save()
    return user


# RPC style
@transaction.atomic
def user_set_password(
    *,
    user: User,
    new_password: str,
    new_password_confirm: Optional[str] = None,
    request: Union[AuthenticatedHttpRequest, None] = None,
) -> None:
    """Set a user's password if they don't have one yet."""
    if user.has_usable_password():
        raise ValidationError(
            [
                _(
                    "User already has a password set. Use password change instead."
                )
            ]
        )

    no_match = (
        new_password_confirm is not None
        and new_password != new_password_confirm
    )
    if no_match:
        raise ValidationError(
            {
                "new_password_confirm": [
                    _("New passwords must match. Please check again")
                ]
            }
        )

    try:
        validate_password(password=new_password, user=user)
    except DjangoValidationError as e:
        raise ValidationError({"new_password": e.messages})

    user.set_password(new_password)
    user.save()

    email = UserPasswordSetEmail(receiver=user, obj=user)
    email.send()

    # Ensure the user stays logged in
    # https://docs.djangoproject.com/en/5.0/topics/auth/default/#session-invalidation-on-password-change
    if request is not None:
        update_session_auth_hash(request, user)


@transaction.atomic
def user_change_password(
    *,
    user: User,
    current_password: str,
    new_password: str,
    # XXX make not Optional
    new_password_confirm: Optional[str] = None,
    request: Union[AuthenticatedHttpRequest, None] = None,
) -> None:
    """Change a user's password."""
    no_match = (
        new_password_confirm is not None
        and new_password != new_password_confirm
    )
    if no_match:
        raise ValidationError(
            {
                "new_password_confirm": [
                    _("New passwords must match. Please check again")
                ]
            }
        )

    if not user.check_password(current_password):
        raise ValidationError(
            {
                "current_password": [
                    _("Incorrect password. Please check again.")
                ]
            }
        )
    try:
        validate_password(password=new_password, user=user)
    except DjangoValidationError as e:
        raise ValidationError({"new_password": e.messages})
    user.set_password(new_password)
    user.save()

    email = UserPasswordChangedEmail(receiver=user, obj=user)
    email.send()

    # Ensure the user stays logged in
    # https://docs.djangoproject.com/en/5.0/topics/auth/default/#session-invalidation-on-password-change
    if request is not None:
        update_session_auth_hash(request, user)


@transaction.atomic
def user_request_email_address_update(
    *,
    user: User,
    new_email: str,
    password: str,
) -> None:
    """Start user email change process."""
    if not user.check_password(password):
        raise ValidationError({"password": [_("Password is incorrect")]})
    user.unconfirmed_email = new_email
    user.save()
    UserEmailAddressUpdateEmail(receiver=user, obj=user).send()


@transaction.atomic
def user_confirm_email_address_update(
    *,
    user: User,
    confirmation_token: Token,
) -> None:
    """Finalize user email change process."""
    old_email = user.email
    new_email = user.unconfirmed_email
    if new_email is None:
        raise ValidationError([_("Email address update was never requested")])
    if not user_check_token(
        user=user, token=confirmation_token, kind="update_email_address"
    ):
        raise ValidationError(
            {"confirmation_token": [_("Provided token is not valid")]}
        )
    user.email = new_email
    user.save()
    PreviousEmailAddress.objects.create(user=user, email=old_email)
    UserEmailAddressUpdatedEmail(receiver=user, obj=user).send()
