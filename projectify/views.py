"""Projectify views."""
from dataclasses import (
    dataclass,
)
from typing import (
    TYPE_CHECKING,
    Union,
)

from strawberry.django import (
    views,
)


if TYPE_CHECKING:
    from user.models import (
        User,
    )


@dataclass
class RequestContext:
    """Request context used in graphql view."""

    user: Union["User", None]
    session: type
    META: dict[str, str]


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
