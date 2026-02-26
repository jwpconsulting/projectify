# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2024-2026 JWP Consulting GK
"""Shared template tags for Projectify."""

import logging
from typing import Any, Literal, Optional, Union

from django import template
from django.contrib.staticfiles import finders
from django.templatetags import static
from django.urls import NoReverseMatch, reverse
from django.utils.html import format_html
from django.utils.safestring import SafeText, mark_safe
from django.utils.translation import gettext_lazy as _

from projectify.user.models import User
from projectify.workspace.models.team_member import TeamMember

logger = logging.getLogger(__name__)

register = template.Library()


@register.filter
def percent(value: Optional[float]) -> Optional[str]:
    """Format value as percentage."""
    if not value:
        return None
    return _("{sub_task_done} %").format(sub_task_done=round(value * 100))


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
            '<span class="sr-only">{text}</span><img class="inline-block w-4 h-4" src="{src}" aria-hidden=true>',
            src=reverse(
                "colored-icon",
                kwargs={"icon": "external_links", "color": "primary"},
            ),
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
def circle_button(
    label: str,
    icon_style: str,
    name: str,
    value: Optional[str] = None,
    disabled: bool = False,
) -> SafeText:
    """Render a circular button."""
    return format_html(
        '<button name="{name}"{value}{disabled} type="submit" hx-swap="outerHTML" '
        'aria-label="{label}"'
        ' class="size-8 p-1.5 rounded-full border border-transparent hover:bg-secondary-hover active:bg-disabled-background disabled:bg-transparent disabled:opacity-20">{icon}</button>',
        name=name,
        disabled=" disabled" if disabled else "",
        value=format_html(' value="{}"', value) if value else "",
        icon=icon(icon_style),
        label=label,
    )


@register.simple_tag
def action_button(
    text: str,
    icon: Optional[str] = None,
    style: Literal["secondary", "destructive"] = "secondary",
    value: Optional[str] = None,
    name: Optional[str] = None,
    grow: bool = True,
    disabled: bool = False,
) -> SafeText:
    """Render a styled action button with icon."""
    # Source: frontend/src/lib/funabashi/buttons/Button.svelte
    color_classes = {
        "secondary": " text-secondary-content hover:bg-secondary-hover hover:text-secondary-content-hover active:bg-secondary-pressed active:text-secondary-content-hover",
        "destructive": " text-destructive hover:bg-destructive-secondary-hover hover:text-destructive-hover active:bg-destructive-secondary-pressed active:text-destructive-pressed",
    }

    return format_html(
        '<button type="submit" '
        'class="{width_class}{color_classes}{disabled_class} flex min-w-0 flex-row justify-center gap-2 rounded-lg px-4 py-2 font-bold"'
        "{disabled_attr}{value}{name}>"
        "{icon}"
        '<span class="truncate">{text}</span>'
        "</button>",
        width_class="w-full" if grow else "",
        color_classes=color_classes[style],
        disabled_class=" opacity-20" if disabled else "",
        disabled_attr=" disabled" if disabled else "",
        icon=format_html(
            '<img class="w-6 h-6 shrink-0" src="{src}" aria-hidden="true">',
            src=reverse(
                "colored-icon",
                kwargs={
                    "icon": icon,
                    "color": "destructive"
                    if style == "destructive"
                    else "primary",
                },
            ),
        )
        if icon
        else "",
        text=text,
        value=format_html(' value="{value}"', value=value) if value else "",
        name=format_html(' name="{name}"', name=name) if name else "",
    )


@register.simple_tag
def icon(
    icon: str,
    color: Optional[Literal["primary", "destructive"]] = None,
    size: Literal[None, 4, 6] = None,
) -> SafeText:
    """Return a rendered heroicon SVG file with optional color."""
    static_path = f"heroicons/{icon}.svg"
    if not finders.find(static_path):
        logger.error("Missing icon '%s'", icon)
        return format_html("<div>MISSING ICON {}</div>", icon)

    if color:
        src = reverse("colored-icon", kwargs={"icon": icon, "color": color})
    else:
        src = static.static(static_path)
    try:
        size_class = (
            format_html(" class={}", {4: "size-4", 6: "size-6"}[size])
            if size
            else ""
        )
    except KeyError:
        logger.error(f"Missing size class for size {size}")
        size_class = ""
    return format_html(
        '<img src="{src}" aria-hidden="true"{size_class}>',
        src=src,
        icon=icon,
        size_class=size_class,
    )


@register.simple_tag
def user_avatar(
    team_member_or_user: Union[None, TeamMember, User],
) -> SafeText:
    """
    Render a user avatar image.

    Takes a user or team member object as parameter.
    """
    match team_member_or_user:
        case TeamMember(user=user) | (User() as user) if user.profile_picture:
            return format_html(
                '<div class="shrink-0 flex flex-row h-6 w-6 items-center rounded-full border border-primary"><img src="{src}" alt="{alt}" height="24" width="24" class="h-full w-full overflow-x-auto rounded-full object-cover object-center"></div>',
                src=user.profile_picture.url,
                alt=str(user),
            )
        case TeamMember(user=user) as team_member:
            avatar_url = reverse(
                "dashboard:avatar-marble", args=[team_member.uuid]
            )
            return format_html(
                '<div class="shrink-0 flex flex-row h-6 w-6 items-center rounded-full border border-primary"><img src="{src}?size=24" alt="{alt}" height="24" width="24" class="h-full w-full overflow-x-auto rounded-full object-cover object-center"></div>',
                src=avatar_url,
                alt=str(user),
            )
        case _:
            return mark_safe(
                '<div class="shrink-0 flex flex-row h-6 w-6 items-center rounded-full border border-primary bg-base-200"></div>'
            )
