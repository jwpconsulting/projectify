# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2024 JWP Consulting GK
"""Shared template tags for Projectify."""

from typing import Optional

from django import template
from django.template.loader import render_to_string
from django.utils.html import format_html
from django.utils.safestring import SafeText
from django.utils.translation import gettext_lazy as _

register = template.Library()


@register.filter
def percent(value: Optional[float]) -> Optional[str]:
    """Format value as percentage."""
    if not value:
        return None
    return f"{value:3.0%}"


@register.simple_tag
def anchor(href: str, label: str, external: bool = False) -> SafeText:
    """
    Render a fully styled HTML anchor.

    Expects label to be translated.
    """
    if external:
        extra = format_html(
            '<span class="sr-only">{text}</span>{svg}',
            svg=render_to_string("heroicons/external_links.svg"),
            text=_("(Opens in new tab)"),
        )
    else:
        extra = ""
    return format_html(
        '<a href="{href}" class="text-primary underline hover:text-primary-hover active:text-primary-pressed text-base">{label}{extra}</a>',
        href=href,
        label=label,
        extra=extra,
    )
