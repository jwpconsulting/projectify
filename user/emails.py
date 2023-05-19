"""User emails."""
from typing import (
    TYPE_CHECKING,
)

from django.contrib import (
    auth,
)

from premail.email import (
    TemplateEmail,
)


if TYPE_CHECKING:
    from user.models import User  # noqa: F401


class UserEmailConfirmationEmail(TemplateEmail["User"]):
    """Email that allows users to confirm their email address."""

    model = auth.get_user_model()
    template_prefix = "user/email/email_confirmation"

    def get_to_email(self) -> str:
        """Return user email."""
        return self.obj.email


class UserPasswordResetEmail(TemplateEmail["User"]):
    """Email that shows a password reset token to the user."""

    model = auth.get_user_model()
    template_prefix = "user/email/password_reset"

    def get_to_email(self) -> str:
        """Return user email."""
        return self.obj.email
