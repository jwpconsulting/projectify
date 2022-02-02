"""Graphql Websocket consumer."""
from django.conf import (
    settings,
)

import channels.auth
import channels_graphql_ws

from . import (
    middleware,
    schema,
)


class GraphqlWsConsumer(channels_graphql_ws.GraphqlWsConsumer):
    """Channels WebSocket consumer which provides GraphQL API."""

    schema = schema.schema

    middleware = [
        middleware.atomic_transaction_middleware,
        middleware.loader_middleware,
    ]

    send_keepalive_every = 30

    strict_ordering = settings.GRAPHQL_WS_SEQUENTIAL

    async def on_connect(self, payload):
        """Handle new client connections."""
        self.scope["user"] = await channels.auth.get_user(self.scope)
