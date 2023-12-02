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
    user_confirm_password_reset,
    user_log_in,
    user_log_out,
    user_request_password_reset,
    user_update,
)

from . import (
    types,
)

if TYPE_CHECKING:
    from ..models import User as _User  # noqa: F401


@strawberry.input
class LoginInput:
    """Login input."""

    email: str
    password: str


@strawberry.input
class RequestPasswordResetInput:
    """RequestPasswordReset input."""

    email: str


@strawberry.input
class ConfirmPasswordResetInput:
    """ConfirmPasswordReset input."""

    email: str
    token: str
    new_password: str


@strawberry.input
class UpdateProfileInput:
    """UpdateProfile input."""

    full_name: str


@strawberry.type
class Mutation:
    """."""

    @strawberry.mutation
    def request_password_reset(self, input: RequestPasswordResetInput) -> str:
        """Mutate."""
        user_request_password_reset(email=input.email)
        return input.email

    @strawberry.mutation
    def confirm_password_reset(
        self,
        input: ConfirmPasswordResetInput,
    ) -> types.User | None:
        """Mutate."""
        return user_confirm_password_reset(
            email=input.email,
            token=input.token,
            new_password=input.new_password,
        )  # type: ignore[return-value]

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
