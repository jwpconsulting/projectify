# SPDX-FileCopyrightText: 2024 JWP Consulting GK
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from typing import (
    Any,
)

from django.core.handlers.asgi import (
    ASGIHandler,
)

from .layers import (
    BaseChannelLayer,
)

class AsyncConsumer:
    scope: dict[str, Any]
    channel_layer: BaseChannelLayer
    channel_name: str

    @classmethod
    def as_asgi(cls, **initkwargs: Any) -> ASGIHandler: ...

class SyncConsumer(AsyncConsumer): ...
