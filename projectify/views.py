"""Projectify views."""
from graphene_django import (
    views,
)

from .loader import (
    Loader,
)


class GraphQLView(views.GraphQLView):
    """Default GraphQLView override."""

    def get_context(self, request):
        """Enhance context with data loaders."""
        request.loader = Loader()
        return request


class GraphQLBatchView(GraphQLView):
    """GraphQL view with batching enabled."""

    batch = True
