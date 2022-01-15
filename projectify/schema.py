"""Projectify project schema."""
from django.conf import (
    settings,
)

import graphene

import channels.auth
import channels_graphql_ws
import user.schema
import workspace.schema


class Query(
    workspace.schema.Query,
    user.schema.Query,
    graphene.ObjectType,
):
    """Query object."""


class Mutation(
    workspace.schema.Mutation,
    user.schema.Mutation,
    graphene.ObjectType,
):
    """Mutation object."""


class Subscription(
    workspace.schema.Subscription,
    graphene.ObjectType,
):
    """Subscription object."""


schema = graphene.Schema(
    query=Query,
    mutation=Mutation,
    subscription=Subscription,
)


class GraphqlWsConsumer(channels_graphql_ws.GraphqlWsConsumer):
    """Channels WebSocket consumer which provides GraphQL API."""

    schema = schema

    send_keepalive_every = 30

    strict_ordering = settings.GRAPHQL_WS_SEQUENTIAL

    async def on_connect(self, payload):
        """Handle new client connections."""
        self.scope["user"] = await channels.auth.get_user(self.scope)
