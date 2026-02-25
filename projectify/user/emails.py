# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2021, 2022, 2023 JWP Consulting GK
"""User emails."""

from django.urls import reverse

from projectify.lib.settings import get_settings
from projectify.premail.email import Context, TemplateEmail
from projectify.user.services.internal import user_make_token

from .models import User


class UserEmailConfirmationEmail(TemplateEmail[User]):
    """Email that allows users to confirm their email address."""

    model = User
    template_prefix = "user/email/email_confirmation"

    def get_context(self) -> Context:
        """Add email confirm token."""
        settings = get_settings()

        email = self.obj.email
        token = user_make_token(user=self.obj, kind="confirm_email_address")
        url = reverse("users:confirm-email", args=(email, token))
        return {
            **super().get_context(),
            "url": f"{settings.FRONTEND_URL}{url}",
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
        settings = get_settings()
        email = self.obj.email
        token = user_make_token(user=self.obj, kind="reset_password")
        url = reverse("users:confirm-password-reset", args=(email, token))
        return {
            **super().get_context(),
            "url": f"{settings.FRONTEND_URL}{url}",
        }


# TODO UserPasswordResetConfirmedEmail
# We want to tell a user that we have reset their password


class UserPasswordChangedEmail(TemplateEmail[User]):
    """Email that tells a user their password changed."""

    model = User
    template_prefix = "user/email/password_changed"


class UserEmailAddressUpdateEmail(TemplateEmail[User]):
    """Email to ask user to confirm email change."""

    model = User
    template_prefix = "user/email/email_address_update"

    @property
    def to(self) -> str:
        """Returns new, unconfirmed email address."""
        match self.receiver:
            case User() if self.receiver.unconfirmed_email:
                return self.receiver.unconfirmed_email
            case _:
                raise ValueError(
                    "Must pass User() with unconfirmed_email as receiver"
                )

    def get_context(self) -> Context:
        """Add reset password token."""
        settings = get_settings()
        token = user_make_token(user=self.obj, kind="update_email_address")
        url = reverse("users:confirm-email-address-update", args=(token,))
        return {
            **super().get_context(),
            "url": f"{settings.FRONTEND_URL}{url}",
            "new_email": self.obj.unconfirmed_email,
        }

    @property
    def addressee(self) -> str:
        """
        Return preferred name of user or email.

        Override is necessary because email goes to new email, but we need
        to reference the user objects name.
        """
        return self.obj.preferred_name or self.obj.email


class UserEmailAddressUpdatedEmail(TemplateEmail[User]):
    """Email to confirm to user that email address was changed."""

    model = User
    template_prefix = "user/email/email_address_updated"

    def get_context(self) -> Context:
        """Add reset password token."""
        return {
            **super().get_context(),
            "new_email": self.obj.email,
        }
