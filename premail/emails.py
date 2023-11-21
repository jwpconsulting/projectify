"""Premail emails."""
from typing import (
    TYPE_CHECKING,
)

from django.contrib import (
    auth,
)

from .email import (
    TemplateEmail,
)

if TYPE_CHECKING:
    from user.models import User  # noqa: F401


class SampleEmail(TemplateEmail["User"]):
    """Sample email for testing."""

    model = auth.get_user_model()
    template_prefix = "premail/email/sample_email"

    def get_to_email(self) -> str:
        """Return user email."""
        return self.obj.email
