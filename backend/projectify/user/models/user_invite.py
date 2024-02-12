# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Copyright (C) 2023 JWP Consulting GK
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
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
