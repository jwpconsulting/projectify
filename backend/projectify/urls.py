# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2021, 2022, 2023 JWP Consulting GK
"""
projectify URL Configuration.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/

Examples
--------
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))


"""

from collections.abc import Sequence
from typing import Union

from django.conf.urls.static import static
from django.contrib import admin
from django.urls import URLPattern, URLResolver, include, path

from projectify.lib.settings import get_settings
from projectify.workspace.consumers import ChangeConsumer

settings = get_settings()

urlpatterns: Sequence[Union[URLResolver, URLPattern]] = (
    # TODO may I use projectify.admin.admin.urls here?
    path("admin/", admin.site.urls),
    path(
        r"user/",
        include("projectify.user.urls"),
    ),
    path(
        "workspace/",
        include("projectify.workspace.urls"),
    ),
    path("corporate/", include("projectify.corporate.urls")),
)

if settings.PREMAIL_PREVIEW:
    urlpatterns = (
        *urlpatterns,
        path(
            r"premail/",
            include("projectify.premail.urls"),
        ),
    )

if settings.SERVE_MEDIA:
    urlpatterns = (
        *urlpatterns,
        *static(
            settings.MEDIA_URL,
            document_root=settings.MEDIA_ROOT,
        ),
    )

if settings.DEBUG_TOOLBAR:
    urlpatterns = (
        *urlpatterns,
        path("__debug__/", include("debug_toolbar.urls")),
    )

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
