# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Copyright (C) 2023-2024 JWP Consulting GK
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""User model services in user app."""
import logging
from typing import Optional

from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from projectify.premail.email import EmailAddress
from projectify.user.emails import (
    UserEmailAddressUpdatedEmail,
    UserEmailAddressUpdateEmail,
    UserPasswordChangedEmail,
)
from projectify.user.models.previous_email_address import PreviousEmailAddress
from projectify.user.models.user import User
from projectify.user.services.internal import Token, user_check_token

logger = logging.getLogger(__name__)


# No Create, since creating users is complicated


# Update
def user_update(
    *,
    who: User,
    user: User,
    preferred_name: Optional[str],
) -> User:
    """Update a user."""
    if not who == user:
        # TODO localize string
        raise PermissionDenied("User can only update own user")
    user.preferred_name = preferred_name
    user.save()
    return user


# RPC style
@transaction.atomic
def user_change_password(
    *,
    user: User,
    current_password: str,
    new_password: str,
) -> None:
    """Change a user's password."""
    if not user.check_password(current_password):
        raise serializers.ValidationError(
            {"current_password": _("Incorrect password. Check again.")}
        )
    user.set_password(new_password)
    user.save()

    email = UserPasswordChangedEmail(receiver=user, obj=user)
    email.send()


@transaction.atomic
def user_request_email_address_update(
    *,
    user: User,
    new_email: str,
    password: str,
) -> None:
    """Start user email change process."""
    if not user.check_password(password):
        raise serializers.ValidationError(
            {"password": _("Password is incorrect")}
        )
    user.unconfirmed_email = new_email
    user.save()
    UserEmailAddressUpdateEmail(
        receiver=EmailAddress(new_email),
        obj=user,
    ).send()


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
        raise serializers.ValidationError(
            _("Email address update was never requested")
        )
    if not user_check_token(
        user=user, token=confirmation_token, kind="update_email_address"
    ):
        raise serializers.ValidationError(
            {"confirmation_token": _("Provided token is not valid")}
        )
    user.email = new_email
    user.save()
    PreviousEmailAddress.objects.create(user=user, email=old_email)
    UserEmailAddressUpdatedEmail(receiver=user, obj=user).send()
