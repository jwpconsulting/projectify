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
from typing import Union

from django.conf.urls.static import static
from django.contrib import admin
from django.urls import URLPattern, URLResolver, include, path
from django.views.generic import TemplateView

from projectify.workspace.consumers import ChangeConsumer

from .lib.settings import get_settings
from .lib.views import (
    colored_icon,
    handler403,
    handler404,
    handler500,
    manifest_view,
)

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
    path(
        "robots.txt",
        TemplateView.as_view(
            template_name="robots.txt", content_type="text/plain; charset=UTF8"
        ),
    ),
    path(
        "humans.txt",
        TemplateView.as_view(
            template_name="humans.txt", content_type="text/plain; charset=UTF8"
        ),
    ),
    path(
        ".well-known/security.txt",
        TemplateView.as_view(
            template_name="well-known-security.txt",
            content_type="text/plain; charset=UTF8",
        ),
    ),
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

if settings.DEBUG_ERROR_PAGES:
    urlpatterns = (
        *urlpatterns,
        path("403.html", handler403),
        path("404.html", handler404),
        path("500.html", handler500),
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


__all__ = ("handler404", "handler500", "handler403")
