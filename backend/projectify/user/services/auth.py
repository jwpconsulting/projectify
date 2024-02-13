# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Copyright (C) 2024 JWP Consulting GK
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
"""User auth services."""
import logging
from typing import Optional

from django.contrib.auth import authenticate, login, logout
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
from projectify.user.services.internal import user_create

logger = logging.getLogger(__name__)


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
            {"tos_agreed": _("Must agree to privacy policy")}
        )

    agreement_dt = timezone.now()

    user = user_create(
        email=email,
        # Here we should validate the password with Django's validation criteria
        password=password,
        tos_agreed=agreement_dt,
        privacy_policy_agreed=agreement_dt,
    )
    mail = UserEmailConfirmationEmail(user)
    mail.send()
    # TODO do not return User here
    return user


def user_confirm_email(
    *,
    email: str,
    token: str,
) -> Optional[User]:
    """Confirm a user's email, return User on success."""
    user = user_find_by_email(email=email)
    if user is None:
        raise serializers.ValidationError(
            {"email": _("No user could be found for this email address")}
        )
    if not user.check_email_confirmation_token(token):
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
) -> Optional[User]:
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
    # XXX consider if returning a user is necessary here
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
    password_reset_email = UserPasswordResetEmail(user)
    password_reset_email.send()


@transaction.atomic
def user_confirm_password_reset(
    *,
    email: str,
    token: str,
    new_password: str,
    # TODO don't return anything here
) -> Optional[User]:
    """Reset a user's password given a new password and a reset token."""
    user = user_find_by_email(email=email)
    if user is None:
        logger.warning(
            "Could not find email %s when attempting to reset a password",
            email,
        )
        raise serializers.ValidationError(
            {"email": _("This email is not recognized")}
        )
    if not user.check_password_reset_token(token):
        logger.warning("Could not match a reset token to email %s", email)
        raise serializers.ValidationError(
            {"token": _("This token is invalid")}
        )
    user.set_password(new_password)
    user.save()
    logger.info("Reset password for user with email %s", email)
    # XXX consider if returning a user is necessary here
    return user
