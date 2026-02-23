# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2021-2025 JWP Consulting GK
"""
Projectify URL Configuration.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/

Several URL patterns are hidden behind a feature flag.

This module also contains a 500 exception handler.
"""

from collections.abc import Sequence
from typing import Optional, Union

from django.conf.urls.static import static
from django.contrib import admin
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden
from django.urls import URLPattern, URLResolver, include, path
from django.utils.translation import gettext_lazy as _

from django_ratelimit.exceptions import Ratelimited

from projectify.lib.settings import get_settings
from projectify.lib.views import colored_icon, manifest_view
from projectify.workspace.consumers import ChangeConsumer

settings = get_settings()

urlpatterns: Sequence[Union[URLResolver, URLPattern]] = (
    # TODO may I use projectify.admin.admin.urls here?
    path("admin/", admin.site.urls),
    path("user/", include("projectify.user.urls")),
    path("workspace/", include("projectify.workspace.urls")),
    path("corporate/", include("projectify.corporate.urls")),
    path(
        "icons/<str:icon>/<str:color>.svg", colored_icon, name="colored-icon"
    ),
    # New Django frontend urls
    path(
        "dashboard/",
        include("projectify.workspace.dashboard_urls"),
    ),
    path(
        "user/",
        include("projectify.user.dashboard_urls"),
    ),
    path("", include("projectify.storefront.urls")),
    path("help/", include("projectify.help.urls")),
    path("onboarding/", include("projectify.onboarding.urls")),
    path("manifest.json", manifest_view, name="manifest"),
)

if settings.PREMAIL_PREVIEW:
    urlpatterns = (
        *urlpatterns,
        path("premail/", include("projectify.premail.urls")),
    )

if settings.SERVE_MEDIA:
    urlpatterns = (
        *urlpatterns,
        *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
    )

if settings.DEBUG_TOOLBAR:
    urlpatterns = (
        *urlpatterns,
        path("__debug__/", include("debug_toolbar.urls")),
    )

if settings.BROWSER_RELOAD:
    urlpatterns = (
        *urlpatterns,
        path("__reload__/", include("django_browser_reload.urls")),
    )

if settings.DEBUG_AUTH:
    urlpatterns = [
        *urlpatterns,
        path("test/", include("projectify.user.testing_urls")),
    ]

if settings.SERVE_SPECTACULAR:
    try:
        from drf_spectacular.views import (
            SpectacularAPIView,
            SpectacularRedocView,
            SpectacularSwaggerView,
        )
    except ImportError as e:
        raise RuntimeError(
            "drf_spectacular was not found. Did you enable SERVE_SPECTACULAR "
            "while running in production?"
        ) from e

    urlpatterns = (
        *urlpatterns,
        path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
        path(
            "api/schema/swagger-ui/",
            SpectacularSwaggerView.as_view(url_name="schema"),
            name="swagger-ui",
        ),
        path(
            "api/schema/redoc/",
            SpectacularRedocView.as_view(url_name="schema"),
            name="redoc",
        ),
    )

websocket_urlpatterns = (
    path("ws/workspace/change", ChangeConsumer.as_asgi()),
)


def handler403(
    request: HttpRequest, exception: Optional[Exception] = None
) -> HttpResponse:
    """Handle Throttled exceptions."""
    del request
    print(f"{exception=}")
    if isinstance(exception, Ratelimited):
        return HttpResponse(_("Too many requests."), status=429)
    return HttpResponseForbidden(_("Forbidden."))
