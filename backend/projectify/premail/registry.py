# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Copyright (C) 2021, 2023 JWP Consulting GK
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
