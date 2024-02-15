# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Copyright (C) 2021, 2022, 2023 JWP Consulting GK
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
"""User emails."""


from projectify.premail.email import (
    Context,
    TemplateEmail,
)
from projectify.user.services.internal import user_make_token

from .models import User


class UserEmailConfirmationEmail(TemplateEmail[User]):
    """Email that allows users to confirm their email address."""

    model = User
    template_prefix = "user/email/email_confirmation"

    def get_context(self) -> Context:
        """Add email confirm token."""
        return {
            **super().get_context(),
            "confirm_email_address_token": user_make_token(
                user=self.obj,
                kind="confirm_email_address",
            ),
        }


# TODO UserEmailConfirmedEmail
# We want to tell a user that we have confirmed their email and that they can
# start using Projectify now


class UserPasswordResetEmail(TemplateEmail[User]):
    """Email that shows a password reset token to the user."""

    model = User
    template_prefix = "user/email/password_reset"

    def get_context(self) -> Context:
        """Add reset password token."""
        return {
            **super().get_context(),
            "reset_password_token": user_make_token(
                user=self.obj,
                kind="reset_password",
            ),
        }


# TODO UserPasswordResetConfirmedEmail
# We want to tell a user that we have reset their password


class UserPasswordChangedEmail(TemplateEmail[User]):
    """Email that tells a user their password changed."""

    model = User
    template_prefix = "user/email/password_changed"
