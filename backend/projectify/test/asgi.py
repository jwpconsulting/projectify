# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2024 JWP Consulting GK
"""Create asgi application optionally wrapped with debug middleware."""

from channels.routing import ProtocolTypeRouter

from projectify.middleware import ErrorChannelator

from ..asgi import asgi_application, websocket_application

websocket_application = ErrorChannelator(websocket_application)

error_application = ProtocolTypeRouter(
    {
        "http": asgi_application,
        "websocket": websocket_application,
    }
)
