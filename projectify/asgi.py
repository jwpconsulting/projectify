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
from django.urls import (
    path,
)

from channels.auth import (
    AuthMiddlewareStack,
)
from channels.routing import (
    ProtocolTypeRouter,
    URLRouter,
)

from .schema import (
    GraphqlWsConsumer,
)


os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", "projectify.settings.production"
)

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AuthMiddlewareStack(
            URLRouter(
                [
                    path("graphql-ws", GraphqlWsConsumer.as_asgi()),
                ],
            ),
        ),
    }
)
