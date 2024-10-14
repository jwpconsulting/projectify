# SPDX-FileCopyrightText: 2024 JWP Consulting GK
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from collections.abc import (
    Sequence,
)
from typing import (
    TypedDict,
)

from django.core.handlers.asgi import (
    ASGIHandler,
)
from django.urls import (
    URLPattern,
)

class ProtocolRoutes(TypedDict):
    http: ASGIHandler
    websocket: ASGIHandler

class URLRouter(ASGIHandler):
    def __init__(self, url: Sequence[URLPattern]) -> None: ...

class ProtocolTypeRouter(ASGIHandler):
    def __init__(self, routes: ProtocolRoutes) -> None: ...
