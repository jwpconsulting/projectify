# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2024 JWP Consulting GK
"""User auth services."""

import logging
from collections.abc import Sequence
from typing import Optional

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import transaction
from django.http import HttpRequest
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from projectify.user.emails import (
    UserEmailConfirmationEmail,
    UserPasswordResetEmail,
)
from projectify.user.models.user import User
from projectify.user.selectors.user import user_find_by_email
from projectify.user.services.internal import (
    Token,
    user_check_token,
    user_create,
)

logger = logging.getLogger(__name__)


# Might be locale dependent, i.e., different languages requiring different
# concatenations.
def _concat_errors(errors: Sequence[str]) -> str:
    return " ".join(errors)


def _validate_password(email: str, password: str) -> None:
    try:
        validate_password(password=password, user=User(email=email))
    except DjangoValidationError as e:
        raise serializers.ValidationError(
            {"password": _concat_errors(e.messages)}
        )


def user_sign_up(
    *,
    email: str,
    password: str,
    tos_agreed: bool,
    privacy_policy_agreed: bool,
) -> User:
    """Sign up a user."""
    # Check if user exists
    if user_find_by_email(email=email) is not None:
        raise serializers.ValidationError(
            {
                "email": _(
                    "A user with this email address is already registered"
                )
            }
        )
    if not tos_agreed:
        raise serializers.ValidationError(
            {"tos_agreed": _("Must agree to terms of service")}
        )
    if not privacy_policy_agreed:
        raise serializers.ValidationError(
            {"privacy_policy_agreed": _("Must agree to privacy policy")}
        )

    _validate_password(email, password)

    agreement_dt = timezone.now()

    user = user_create(
        email=email,
        password=password,
        tos_agreed=agreement_dt,
        privacy_policy_agreed=agreement_dt,
    )
    mail = UserEmailConfirmationEmail(receiver=user, obj=user)
    mail.send()
    # TODO do not return User here
    return user


def user_confirm_email(
    *,
    email: str,
    token: Token,
) -> Optional[User]:
    """Confirm a user's email, return User on success."""
    user = user_find_by_email(email=email)
    if user is None:
        raise serializers.ValidationError(
            {"email": _("No user could be found for this email address")}
        )
    if not user_check_token(
        user=user, kind="confirm_email_address", token=token
    ):
        raise serializers.ValidationError(
            {"token": _("This email confirmation token is invalid")}
        )
    user.is_active = True
    user.save()
    # TODO do not return User here
    return user


def user_log_in(
    *,
    email: str,
    password: str,
    request: HttpRequest,
) -> User:
    """Log a user in, return cookies."""
    user = authenticate(request, username=email, password=password)
    if user is None:
        maybe_user = user_find_by_email(email=email)
        if maybe_user is None:
            logger.warning("Could not find a user for %s", email)
            raise serializers.ValidationError(
                {"email": _("No user could be found for this email address")}
            )
        if not maybe_user.is_active:
            logger.warning(
                "Tried to log in for inactive user with email %s", email
            )
            raise serializers.ValidationError(
                {
                    "email": _(
                        "This email address has not been confirmed. "
                        "Please check your email inbox for a confirmation email or contact our support if you need further help."
                    )
                }
            )
        logger.warning(
            "User with email %s found but authentication failed", email
        )
        raise serializers.ValidationError(
            {"password": _("The password is incorrect. Please try again.")}
        )
    login(request, user)
    if not isinstance(user, User):
        raise ValueError("User is not User, why?")
    return user


def user_log_out(
    *,
    request: HttpRequest,
) -> None:
    """Log a user out, update cookies."""
    user = request.user
    if user.is_anonymous:
        raise serializers.ValidationError(_("There is no logged in user"))
    logout(request)


def user_request_password_reset(
    *,
    # Should this be taking in a user object instead?
    email: str,
) -> None:
    """Send a password reset email to a user, given their email address."""
    user = user_find_by_email(email=email)
    if user is None:
        raise serializers.ValidationError(
            {"email": _("No user could be found for this email")}
        )
    password_reset_email = UserPasswordResetEmail(receiver=user, obj=user)
    password_reset_email.send()


@transaction.atomic
def user_confirm_password_reset(
    *,
    email: str,
    token: Token,
    new_password: str,
    new_password_confirm: Optional[str] = None,
    # TODO don't return anything here
) -> Optional[User]:
    """Reset a user's password given a new password and a reset token."""
    if new_password_confirm is not None:
        if new_password != new_password_confirm:
            raise serializers.ValidationError(
                {
                    "new_password_confirm": _(
                        "New passwords must match. Please check again"
                    )
                }
            )

    user = user_find_by_email(email=email)
    if user is None:
        logger.warning(
            "Could not find email %s when attempting to reset a password",
            email,
        )
        raise serializers.ValidationError(
            {"email": _("This email is not recognized")}
        )
    if not user_check_token(user=user, token=token, kind="reset_password"):
        logger.warning("Could not match a reset token to email %s", email)
        raise serializers.ValidationError(
            {"token": _("This token is invalid")}
        )
    user.set_password(new_password)
    user.save()
    logger.info("Reset password for user with email %s", email)
    # XXX consider if returning a user is necessary here
    return user
