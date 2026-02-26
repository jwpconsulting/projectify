# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2026 JWP Consulting GK
"""Projectify general views."""

import logging
from pathlib import Path
from typing import Optional

from django.contrib.staticfiles import finders
from django.contrib.staticfiles.storage import staticfiles_storage
from django.http import (
    Http404,
    HttpRequest,
    HttpResponse,
    HttpResponseForbidden,
    JsonResponse,
)
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django.views.decorators.cache import cache_control

from django_ratelimit.exceptions import Ratelimited

logger = logging.getLogger(__name__)


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


def manifest_view(request: HttpRequest) -> JsonResponse:
    """Return the web app manifest.json."""
    del request
    manifest_data = {
        "name": "Projectify",
        "short_name": "Projectify",
        "description": "Free open source project management software",
        "dir": "auto",
        "lang": "en-US",
        "display": "standalone",
        "orientation": "any",
        "start_url": "/?homescreen=1",
        "background_color": "#fff",
        "theme_color": "#fff",
        "icons": [
            {
                "src": staticfiles_storage.url("favicon.ico"),
                "sizes": "32x32",
                "type": "image/x-icon",
                "purpose": "any",
            },
            {
                "src": staticfiles_storage.url("apple-touch-icon.png"),
                "sizes": "180x180",
                "type": "image/png",
                "purpose": "any",
            },
        ],
        "shortcuts": [
            {
                "name": "View Projectify Dashboard",
                "short_name": "Dashboard",
                "description": "View your Projectify dashboard",
                "url": "/dashboard",
                "icons": [
                    {
                        "src": staticfiles_storage.url("apple-touch-icon.png"),
                        "sizes": "180x180",
                        "type": "image/png",
                    }
                ],
            }
        ],
    }
    return JsonResponse(manifest_data)


def handler403(
    request: HttpRequest, exception: Optional[Exception] = None
) -> HttpResponse:
    """Handle Throttled exceptions."""
    del request
    if isinstance(exception, Ratelimited):
        return HttpResponse(_("Too many requests."), status=429)
    return HttpResponseForbidden(_("Forbidden."))


def handler404(
    request: HttpRequest, exception: Optional[Exception] = None
) -> HttpResponse:
    """Handle 404 errors with a custom page."""
    if exception:
        context = {"error": str(exception)}
    else:
        context = {}
    logger.warning("Handling 404 error for exception=%s", exception)
    return render(request, "404.html", status=404, context=context)


def handler500(request: HttpRequest) -> HttpResponse:
    """Handle 500 errors with a custom page."""
    return render(request, "500.html", status=500)
