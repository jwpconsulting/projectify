# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2024 JWP Consulting GK
"""Shared template tags for Projectify."""

from django import template

register = template.Library()


@register.filter
def percent(value: float) -> str:
    """Format value as percentage."""
    return f"{value:3.0%}"
