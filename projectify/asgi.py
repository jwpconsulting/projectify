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
ASGI config for projectify project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from channels.auth import (
    AuthMiddlewareStack,
)
from channels.routing import (
    ProtocolTypeRouter,
    URLRouter,
)
from configurations.asgi import (
    get_asgi_application,
)

# TODO still needed? We should just let the server crash when this env var is
# unset
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", "projectify.settings.production"
)
asgi_application = get_asgi_application()

# I believe we had to move this down here so that all applications can be
# mounted correctly, since importing the URLs could otherwise import views
# that use unitialized Django models. Justus 2023-10-18
from .urls import (  # noqa: E402
    websocket_urlpatterns,
)

websocket_application = AuthMiddlewareStack(URLRouter(websocket_urlpatterns))

application = ProtocolTypeRouter(
    {
        "http": asgi_application,
        "websocket": websocket_application,
    }
)
