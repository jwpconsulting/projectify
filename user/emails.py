"""User emails."""
from django.contrib import (
    auth,
)

from premail.email import (
    TemplateEmail,
)


class UserEmailConfirmationEmail(TemplateEmail):
    """Email that allows users to confirm their email address."""

    model = auth.get_user_model()
    template_prefix = "user/email/email_confirmation"
