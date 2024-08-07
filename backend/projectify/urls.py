# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Copyright (C) 2021, 2022, 2023 JWP Consulting GK
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
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
        r"premail/",
        include("projectify.premail.urls"),
    ),
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
