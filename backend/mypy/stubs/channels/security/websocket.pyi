"""Bindings for channels.security.websocket."""
from django.core.handlers.asgi import (
    ASGIHandler,
)

from channels.middleware import (
    BaseMiddleware,
)

class AllowedHostsOriginValidator(BaseMiddleware):
    def __init__(self, inner: ASGIHandler) -> None: ...
