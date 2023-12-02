"""User schema mutations."""
from typing import (
    TYPE_CHECKING,
    cast,
)

import strawberry
from graphql import (
    GraphQLResolveInfo,
)

from user.services.user import (
    user_update,
)

from . import (
    types,
)

if TYPE_CHECKING:
    from ..models import User as _User  # noqa: F401


@strawberry.input
class UpdateProfileInput:
    """UpdateProfile input."""

    full_name: str


@strawberry.type
class Mutation:
    """."""

    @strawberry.mutation
    def update_profile(
        self,
        input: UpdateProfileInput,
        info: GraphQLResolveInfo,
    ) -> types.User | None:
        """Mutate."""
        user = cast("_User", info.context.user)
        if not user.is_authenticated:
            # Inaccurate, this method should only ever be callable when
            # authenticated
            return None
        return user_update(
            who=user,
            user=user,
            full_name=input.full_name,
        )  # type: ignore[return-value]
