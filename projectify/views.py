"""Projectify views."""
from dataclasses import (
    dataclass,
)
from typing import (
    Union,
)

from django.contrib.auth.models import (
    AbstractBaseUser,
    AnonymousUser,
)

from strawberry.django import (
    views,
)


@dataclass
class RequestContext:
    """Request context used in graphql view."""

    user: Union[AnonymousUser, AbstractBaseUser, None]
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
