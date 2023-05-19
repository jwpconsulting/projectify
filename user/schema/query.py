"""User schema queries."""
import strawberry

from graphql import (
    GraphQLResolveInfo,
)

from . import (
    types,
)


@strawberry.type
class Query:
    """Query."""

    @strawberry.field(types.User)
    def user(self, info: GraphQLResolveInfo) -> types.User | None:
        """Resolve user field."""
        user = info.context.user
        if user.is_authenticated:
            return user  # type: ignore
        return None
