"""User schema queries."""
import graphene

from . import (
    types,
)


class Query:
    """Query."""

    user = graphene.Field(types.User)

    def resolve_user(self, info):
        """Resolve user field."""
        user = info.context.user
        if user.is_authenticated:
            return user
