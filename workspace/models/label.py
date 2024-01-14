# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Copyright (C) 2023-2024 JWP Consulting GK
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
"""Label manager and model."""
import uuid
from typing import (
    TYPE_CHECKING,
    ClassVar,
    Self,
    cast,
)

from django.contrib.auth.models import (
    AbstractBaseUser,
)
from django.db import (
    models,
)
from django.utils.translation import gettext_lazy as _

from projectify.lib.models import BaseModel

from .types import (
    Pks,
)
from .workspace import Workspace as Workspace

# TODO Here we could be using __all__


class LabelQuerySet(models.QuerySet["Label"]):
    """Label Queryset."""

    def filter_by_workspace_pks(self, workspace_pks: Pks) -> Self:
        """Filter by workspace pks."""
        return self.filter(workspace__pk__in=workspace_pks)

    def filter_for_user_and_uuid(
        self, user: AbstractBaseUser, uuid: uuid.UUID
    ) -> Self:
        """Return for matching workspace user and uuid."""
        return self.filter(workspace__users=user, uuid=uuid)


class Label(BaseModel):
    """A label."""

    # TODO It should be fine to just use TitleDescription here
    name = models.CharField(max_length=255)
    color = models.PositiveBigIntegerField(
        help_text=_("Color index"),
        default=0,
    )
    workspace = models.ForeignKey[Workspace](
        Workspace,
        on_delete=models.CASCADE,
    )
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)

    objects: ClassVar[LabelQuerySet] = cast(  # type: ignore[assignment]
        LabelQuerySet, LabelQuerySet.as_manager()
    )

    if TYPE_CHECKING:
        id: int

    def __str__(self) -> str:
        """Return name."""
        return self.name

    class Meta:
        """Meta."""

        # TODO remove this restriction, just let users do what they want to
        unique_together = ("workspace", "name")
