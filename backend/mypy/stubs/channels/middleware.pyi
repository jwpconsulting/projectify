from django.core.handlers.asgi import (
    ASGIHandler,
)

class BaseMiddleware(ASGIHandler):
    def __init__(self, inner: BaseMiddleware) -> None: ...
