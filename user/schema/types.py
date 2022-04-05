"""User schema types."""
from django.contrib import (
    auth,
)

import strawberry


@strawberry.django.type(auth.get_user_model())
class User:
    """User."""

    email: str
    full_name: str | None

    @strawberry.field
    def profile_picture(self) -> str | None:
        """Resolve profile_picture."""
        if self.profile_picture:
            return self.profile_picture.url
