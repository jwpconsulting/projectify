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

from projectify.user.models.user import User

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

    Set external=True when you want the link to open
    """
    if external:
        a_extra = 'target="_blank"'
        extra = format_html(
            '<span class="sr-only">{text}</span>{svg}',
            svg=render_to_string("heroicons/external_links.svg"),
            text=_("(Opens in new tab)"),
        )
    else:
        a_extra = ""
        extra = ""
    return format_html(
        '<a href="{href}" class="text-primary underline hover:text-primary-hover active:text-primary-pressed text-base"{a_extra}>{label}{extra}</a>',
        a_extra=a_extra,
        href=href,
        label=label,
        extra=extra,
    )


@register.simple_tag
def user_avatar(user: User) -> SafeText:
    """
    Render a user avatar image.

    Takes a user object as parameter.
    """
    if user.profile_picture:
        return format_html(
            '<div class="shrink-0 flex flex-row h-6 w-6 items-center rounded-full border border-primary"><img src="{src}" alt="{alt}" height="24" width="24" class="h-full w-full overflow-x-auto rounded-full object-cover object-center"></div>',
            src=user.profile_picture.url,
            alt=str(user),
        )
    else:
        return format_html("")
