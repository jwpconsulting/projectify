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
from typing import (
    Iterable,
    Union,
)

from django.conf import (
    settings,
)
from django.conf.urls.static import (
    static,
)
from django.contrib import (
    admin,
)
from django.urls import (
    URLPattern,
    URLResolver,
    include,
    path,
)

from workspace.consumers import (
    TaskConsumer,
    WorkspaceBoardConsumer,
    WorkspaceConsumer,
)

urlpatterns: Iterable[Union[URLResolver, URLPattern]] = (
    path("admin/", admin.site.urls),
    path(
        r"premail/",
        include("premail.urls"),
    ),
    path(
        r"user/",
        include("user.urls"),
    ),
    path(
        "workspace/",
        include("workspace.urls"),
    ),
    path("blog/api/v1/", include("blog.urls")),
    path("corporate/", include("corporate.urls")),
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

websocket_urlpatterns = (
    path("ws/task/<uuid:uuid>/", TaskConsumer.as_asgi()),
    path("ws/workspace-board/<uuid:uuid>/", WorkspaceBoardConsumer.as_asgi()),
    path("ws/workspace/<uuid:uuid>/", WorkspaceConsumer.as_asgi()),
)
