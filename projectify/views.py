"""Projectify views."""
from graphene_django import (
    views,
)


class GraphQLView(views.GraphQLView):
    """Default GraphQLView override."""


class GraphQLBatchView(GraphQLView):
    """GraphQL view with batching enabled."""

    batch = True
