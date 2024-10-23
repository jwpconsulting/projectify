# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2021, 2023 JWP Consulting GK
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
    from projectify.user.models import User  # noqa: F401


class SampleEmail(TemplateEmail["User"]):
    """Sample email for testing."""

    model = auth.get_user_model()
    template_prefix = "premail/email/sample_email"
