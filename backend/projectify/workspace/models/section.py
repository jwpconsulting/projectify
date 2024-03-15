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
"""Section model."""
import uuid
from typing import (
    TYPE_CHECKING,
    Callable,
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

from django_extensions.db.models import (
    TitleDescriptionModel,
)

from projectify.lib.models import BaseModel

from .task import (
    Task,
)
from .types import (
    GetOrder,
    Pks,
    SetOrder,
)

if TYPE_CHECKING:
    from django.db.models.manager import RelatedManager  # noqa: F401

    from . import Project  # noqa: F401


class SectionQuerySet(models.QuerySet["Section"]):
    """QuerySet for Project."""

    def filter_by_project_pks(self, keys: Pks) -> Self:
        """Filter by projects."""
        return self.filter(project__pk__in=keys)

    def filter_for_user_and_uuid(
        self, user: AbstractBaseUser, uuid: uuid.UUID
    ) -> Self:
        """Return a workspace for user and uuid."""
        return self.filter(project__workspace__users=user, uuid=uuid)


class Section(TitleDescriptionModel, BaseModel):
    """Section of a Project."""

    project = models.ForeignKey["Project"](
        "Project",
        on_delete=models.CASCADE,
    )
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    objects: ClassVar[SectionQuerySet] = cast(  # type: ignore[assignment]
        SectionQuerySet,
        SectionQuerySet.as_manager(),
    )

    if TYPE_CHECKING:
        # Related managers
        task_set: RelatedManager["Task"]

        # For ordering
        get_task_order: GetOrder
        set_task_order: SetOrder
        get_next_in_order: Callable[[], "Section"]
        _order: int

    def __str__(self) -> str:
        """Return title."""
        return self.title

    class Meta:
        """Meta."""

        order_with_respect_to = "project"
        constraints = [
            models.UniqueConstraint(
                fields=["project", "_order"],
                name="unique_project_order",
                deferrable=models.Deferrable.DEFERRED,
            )
        ]
