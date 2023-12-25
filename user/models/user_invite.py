"""User invite model in user app."""
from typing import (
    ClassVar,
    cast,
)

from django.conf import (
    settings,
)
from django.db import (
    models,
)
from django.utils.translation import gettext_lazy as _

from typing_extensions import (
    Self,
)

from projectify.lib.models import BaseModel

from .user import User


class UserInviteQuerySet(models.QuerySet["UserInvite"]):
    """User invite QuerySet."""

    def is_redeemed(self, redeemed: bool = True) -> Self:
        """Return not self redeemed invites."""
        return self.filter(redeemed=redeemed)

    def by_email(self, email: str) -> Self:
        """Filter by email."""
        return self.filter(email=email)


class UserInvite(BaseModel):
    """User invite model."""

    email = models.EmailField(
        verbose_name=_("Email"),
    )
    user = models.ForeignKey[User](
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        help_text=_("Matched user"),
    )
    redeemed = models.BooleanField(
        default=False,
        help_text=_("Has this invite been redeemed?"),
    )

    objects: ClassVar[UserInviteQuerySet] = cast(  # type: ignore[assignment]
        UserInviteQuerySet, UserInviteQuerySet.as_manager()
    )
