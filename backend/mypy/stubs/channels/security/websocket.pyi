"""Bindings for channels.security.websocket."""

from collections.abc import Sequence

from django.core.handlers.asgi import (
    ASGIHandler,
)

from channels.middleware import (
    BaseMiddleware,
)

class OriginValidator(BaseMiddleware):
    def __init__(
        self, inner: ASGIHandler, allowed_origins: Sequence[str]
    ) -> None: ...

class AllowedHostsOriginValidator(OriginValidator):
    def __init__(self, inner: ASGIHandler) -> None: ...
