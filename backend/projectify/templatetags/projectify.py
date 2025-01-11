# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2024 JWP Consulting GK
"""Shared template tags for Projectify."""

from typing import Optional

from django import template

register = template.Library()


@register.filter
def percent(value: Optional[float]) -> Optional[str]:
    """Format value as percentage."""
    if not value:
        return None
    return f"{value:3.0%}"
