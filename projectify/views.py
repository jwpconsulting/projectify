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
from django.contrib.sessions.backends.base import (
    SessionBase,
)
from django.http import (
    HttpRequest,
    HttpResponse,
)

from strawberry.django import (
    views,
)


@dataclass
class RequestContext:
    """Request context used in graphql view."""

    user: Union[AnonymousUser, AbstractBaseUser, None]
    session: SessionBase
    META: dict[str, str]


# projectify/views.py:35: error: Missing type parameters for generic type "GraphQLView"  [type-arg]
# Why? XXX Justus 2023-09-08
class GraphQLView(views.GraphQLView):  # type: ignore
    """Default GraphQLView override."""

    def get_context(
        self, request: HttpRequest, response: HttpResponse
    ) -> RequestContext:
        """Populate request context with useful variables."""
        return RequestContext(
            user=request.user,
            session=request.session,
            META=request.META,
        )
