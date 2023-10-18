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
