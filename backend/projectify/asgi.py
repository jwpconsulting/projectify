# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2021, 2022, 2023 JWP Consulting GK
"""
ASGI config for projectify project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

from configurations.asgi import (  # type: ignore[attr-defined]
    get_asgi_application,
)
from projectify.middleware import CsrfTrustedOriginsOriginValidator

# TODO still needed? We should just let the server crash when this env var is
# unset
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", "projectify.settings.production"
)
asgi_application = get_asgi_application()

# I believe we had to move this down here so that all applications can be
# mounted correctly, since importing the URLs could otherwise import views
# that use unitialized Django models. Justus 2023-10-18
from .urls import websocket_urlpatterns  # noqa: E402

websocket_application = CsrfTrustedOriginsOriginValidator(
    AuthMiddlewareStack(URLRouter(websocket_urlpatterns))
)

application = ProtocolTypeRouter(
    {
        "http": asgi_application,
        "websocket": websocket_application,
    }
)


__all__ = ("application",)
