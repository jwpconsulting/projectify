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
"""Chat message model."""
import uuid
from typing import (
    ClassVar,
    Self,
    cast,
)

from django.contrib.auth.models import AbstractBaseUser
from django.db import (
    models,
)

from projectify.lib.models import BaseModel

from .task import (
    Task,
)
from .types import Pks
from .workspace_user import (
    WorkspaceUser,
)


class ChatMessageQuerySet(models.QuerySet["ChatMessage"]):
    """ChatMessage query set."""

    def filter_by_task_pks(self, task_pks: Pks) -> Self:
        """Filter by task pks."""
        return self.filter(task__pk__in=task_pks)

    def filter_for_user_and_uuid(
        self, user: AbstractBaseUser, uuid: uuid.UUID
    ) -> Self:
        """Get for a specific workspace user and uuid."""
        kwargs = {
            "task__workspace_board_section__workspace_board__"
            "workspace__users": user,
            "uuid": uuid,
        }
        return self.filter(**kwargs)


class ChatMessage(BaseModel):
    """ChatMessage, belongs to Task."""

    task = models.ForeignKey["Task"](
        Task,
        on_delete=models.CASCADE,
    )
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    text = models.TextField()
    author = models.ForeignKey["WorkspaceUser"](
        WorkspaceUser,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    # XXX
    objects: ClassVar[ChatMessageQuerySet] = cast(  # type: ignore[assignment]
        ChatMessageQuerySet, ChatMessageQuerySet.as_manager()
    )

    class Meta:
        """Meta."""

        ordering = ("created",)
