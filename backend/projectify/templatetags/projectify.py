# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2024 JWP Consulting GK
"""Shared template tags for Projectify."""

from typing import Optional

from django import template
from django.utils.html import format_html
from django.utils.safestring import SafeText

register = template.Library()


@register.filter
def percent(value: Optional[float]) -> Optional[str]:
    """Format value as percentage."""
    if not value:
        return None
    return f"{value:3.0%}"


@register.simple_tag
def anchor(href: str, label: str) -> SafeText:
    """
    Render a fully styled HTML anchor.

    Expects label to be translated.
    """
    return format_html(
        '<a href="{href}" class="text-primary underline hover:text-primary-hover active:text-primary-pressed text-base">{label}</a>',
        href=href,
        label=label,
    )
