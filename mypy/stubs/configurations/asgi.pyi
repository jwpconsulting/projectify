from django.core.handlers.asgi import (
    ASGIHandler,
)

def get_asgi_application() -> ASGIHandler: ...
