# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2026 JWP Consulting GK
"""View decorators."""

import logging
from pathlib import Path
from typing import Any, Protocol

from django.contrib.auth.decorators import login_required
from django.contrib.staticfiles import finders
from django.http import Http404, HttpRequest, HttpResponse
from django.views.decorators.cache import cache_control

from projectify.lib.types import AuthenticatedHttpRequest

logger = logging.getLogger(__name__)


class LoggedInViewP(Protocol):
    """Django view method that takes an AuthenticatedHttpRequest."""

    def __call__(
        self, request: AuthenticatedHttpRequest, *args: Any, **kwargs: Any
    ) -> HttpResponse:
        """Take a request and respond."""
        ...


def platform_view(func: LoggedInViewP) -> LoggedInViewP:
    """
    Wrap view in login_required.

    This makes it easier to add required decorators or other things to views
    that are part of the platform, i.e., pages that require the user to be
    logged in.
    """
    return login_required(func)


@cache_control(max_age=3600)
def colored_icon(request: HttpRequest, icon: str, color: str) -> HttpResponse:
    """Return a colored SVG icon."""
    del request
    # See `const colors` projectify/theme/static_src/tailwind.config.js
    color_map = {
        "primary": "#2563EB",
        "destructive": "#dc2626",
        "white": "#ffffff",
    }

    match finders.find(f"heroicons/{icon}.svg"):
        case list() as paths:
            raise ValueError(
                f"Tried to look for icon {icon}, got a list of paths {paths}"
            )
        case None:
            raise Http404(f"Icon '{icon}' not found")
        case str() as icon_path:
            pass

    if color not in color_map:
        raise Http404(f"Missing color '{color}' for icon '{icon}'")

    svg_content = (
        Path(icon_path)
        .read_text()
        .replace("<svg", f'<svg style="color: {color_map[color]}"')
    )
    return HttpResponse(svg_content, content_type="image/svg+xml")
