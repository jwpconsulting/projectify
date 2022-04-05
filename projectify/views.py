"""Projectify views."""
from dataclasses import (
    dataclass,
)

from django.contrib.auth import (
    get_user_model,
)

from strawberry.django import (
    views,
)


@dataclass
class RequestContext:
    """Request context used in graphql view."""

    user: get_user_model() | None
    session: type
    META: dict


class GraphQLView(views.GraphQLView):
    """Default GraphQLView override."""

    def get_context(self, request, response):
        """Populate request context with useful variables."""
        return RequestContext(
            user=request.user,
            session=request.session,
            META=request.META,
        )


class GraphQLBatchView(GraphQLView):
    """GraphQL view with batching enabled."""

    # TODO
