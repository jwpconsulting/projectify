# SPDX-FileCopyrightText: 2024 JWP Consulting GK
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from django.core.handlers.asgi import (
    ASGIHandler,
)

class BaseMiddleware(ASGIHandler):
    def __init__(self, inner: BaseMiddleware) -> None: ...
