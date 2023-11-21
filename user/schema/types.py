"""User schema types."""
from typing import (
    TYPE_CHECKING,
    cast,
)

from django.contrib import (
    auth,
)

import strawberry

if TYPE_CHECKING:
    from ..models import User as _User  # noqa: F401


@strawberry.django.type(auth.get_user_model())
class User:
    """User."""

    email: str
    full_name: str | None

    @strawberry.field
    def profile_picture(self) -> str | None:
        """Resolve profile_picture."""
        user = cast("_User", self)
        if user.profile_picture:
            return user.profile_picture.url
        return None
