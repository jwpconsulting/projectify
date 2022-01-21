"""
ASGI config for projectify project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import (
    get_asgi_application,
)

from channels.auth import (
    AuthMiddlewareStack,
)
from channels.routing import (
    ProtocolTypeRouter,
    URLRouter,
)


os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", "projectify.settings.production"
)
asgi_application = get_asgi_application()

from .urls import (  # noqa: E402
    websocket_urlpatterns,
)


application = ProtocolTypeRouter(
    {
        "http": asgi_application,
        "websocket": AuthMiddlewareStack(
            URLRouter(websocket_urlpatterns),
        ),
    }
)
