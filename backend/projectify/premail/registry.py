# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2021, 2023 JWP Consulting GK
"""Premail email registry."""

import importlib
import inspect
from typing import Any

from django.apps import (
    apps,
)

from .email import (
    TemplateEmail,
)

registry: dict[str, Any] = {
    # 'user-email-confirmation': user_emails.UserEmailConfirmationEmail,
}


def add_members(emails: object) -> None:
    """Add email templates to registry."""
    for name, obj in inspect.getmembers(emails):
        is_candidate = (
            inspect.isclass(obj)
            and obj is not TemplateEmail
            and issubclass(obj, TemplateEmail)
        )
        if is_candidate:
            registry[name] = obj


for app in apps.app_configs:
    try:
        emails = importlib.import_module(f"projectify.{app}.emails")
    except ModuleNotFoundError:
        continue
    add_members(emails)
