from django.core.handlers.asgi import (
    ASGIHandler,
)

from channels.middleware import (
    BaseMiddleware,
)

class AuthMiddlewareStack(BaseMiddleware):
    def __init__(self, inner: ASGIHandler) -> None: ...
