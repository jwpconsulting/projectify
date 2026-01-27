# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2024 JWP Consulting GK
"""Shared template tags for Projectify."""

from typing import Any, Literal, Optional, Union

from django import template
from django.template.loader import render_to_string
from django.urls import NoReverseMatch, reverse
from django.utils.html import format_html
from django.utils.safestring import SafeText, mark_safe
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
def anchor(
    href: str, label: str, external: bool = False, *args: Any, **kwargs: Any
) -> SafeText:
    """
    Render a fully styled HTML anchor.

    Expects label to be translated.

    Set external=True when you want the link to open
    """
    extra: Union[SafeText, str]
    a_extra: Union[SafeText, str]
    if href == "":
        raise ValueError("Empty href supplied")
    try:
        url = reverse(href, args=args, kwargs=kwargs)
    except NoReverseMatch:
        url = href
    # TODO, if we have a reverse match, we don't have external URLs
    # We could switch all callers of the anchor function to use the route name
    # and implicitly switch on external for all other URLs. After all, if it's
    # an internal resource, we'd have a named route for that resource.
    if external:
        a_extra = mark_safe(' target="_blank"')
        extra = format_html(
            '<span class="sr-only">{text}</span>{svg}',
            svg=render_to_string("heroicons/external_links.svg"),
            text=_("(Opens in new tab)"),
        )
    else:
        a_extra = ""
        extra = ""
    return format_html(
        '<a href="{url}" class="text-primary underline hover:text-primary-hover active:text-primary-pressed text-base"{a_extra}>{label}{extra}</a>',
        a_extra=a_extra,
        url=url,
        label=label,
        extra=extra,
    )


@register.simple_tag
def action_button(
    text: str,
    icon: Optional[str] = None,
    style: Literal["primary", "destructive"] = "primary",
    value: Optional[str] = None,
    name: Optional[str] = None,
    grow: bool = True,
) -> SafeText:
    """Render a styled action button with icon."""
    # Source: frontend/src/lib/funabashi/buttons/Button.svelte
    color_classes = {
        "primary": "text-secondary-content hover:bg-secondary-hover hover:text-secondary-content-hover active:bg-secondary-pressed active:text-secondary-content-hover",
        "destructive": "text-destructive hover:bg-destructive-secondary-hover hover:text-destructive-hover active:bg-destructive-secondary-pressed active:text-destructive-pressed",
    }

    return format_html(
        '<button type="submit" '
        'class="{width_class} {color_classes} flex min-w-max flex-row justify-center gap-2 rounded-lg px-4 py-2 font-bold"'
        "{value}{name}>"
        "{icon}"
        "{text}"
        "</button>",
        width_class="w-full" if grow else "min-w-max",
        color_classes=color_classes[style],
        icon=format_html('<div class="w-6 h-6">{icon}</div>', icon=render_to_string(f"heroicons/{icon}.svg")) if icon else '',
        text=text,
        value=format_html(' value="{value}"', value=value) if value else "",
        name=format_html(' name="{name}"', name=name) if name else "",
    )


@register.simple_tag
def user_avatar(user: Optional[User]) -> SafeText:
    """
    Render a user avatar image.

    Takes a user object as parameter.
    """
    if user and user.profile_picture:
        return format_html(
            '<div class="shrink-0 flex flex-row h-6 w-6 items-center rounded-full border border-primary"><img src="{src}" alt="{alt}" height="24" width="24" class="h-full w-full overflow-x-auto rounded-full object-cover object-center"></div>',
            src=user.profile_picture.url,
            alt=str(user),
        )
    # TODO improve appearance
    elif user:
        return format_html(
            '<div class="shrink-0 flex flex-row h-6 w-6 items-center rounded-full border border-primary" aria-label="{alt}"></div>',
            alt=str(user),
        )
    else:
        return mark_safe(
            '<div class="shrink-0 flex flex-row h-6 w-6 items-center rounded-full border border-primary bg-base-200"></div>'
        )
