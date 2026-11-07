# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2026 JWP Consulting GK
"""Test views to easily access general Projectify pages."""

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse

from projectify.lib.settings import get_settings

settings = get_settings()
assert settings.DEBUG_AUTH, "Can't import this if DEBUG_AUTH isn't set"


def debug_error_pages(request: HttpRequest) -> HttpResponse:
    """Return overview of available error pages."""
    error_pages = [
        (reverse("400.html"), "400 Bad Request"),
        (reverse("403.html"), "403 Forbidden"),
        (reverse("403_csrf.html"), "403 CSRF Failure"),
        (reverse("404.html"), "404 Not Found"),
        (reverse("500.html"), "500 Internal Server Error"),
    ]
    return render(
        request, "test/debug_error_pages.html", {"error_pages": error_pages}
    )
