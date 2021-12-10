"""Premail emails."""
from django.contrib import (
    auth,
)

from .email import (
    TemplateEmail,
)


class SampleEmail(TemplateEmail):
    """Sample email for testing."""

    model = auth.get_user_model()
    template_prefix = "premail/email/sample_email"
