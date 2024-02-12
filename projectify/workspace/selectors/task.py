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
"""Workspace selectors."""

from typing import Optional
from uuid import UUID

from django.db.models import Prefetch

from projectify.user.models import User
from projectify.workspace.models.chat_message import ChatMessage
from projectify.workspace.models.task import Task, TaskQuerySet

TaskDetailQuerySet: TaskQuerySet = (
    Task.objects.select_related(
        "workspace_board_section__workspace_board__workspace",
        "assignee",
        "assignee__user",
    )
    .prefetch_related(
        "labels",
        "subtask_set",
    )
    .prefetch_related(
        Prefetch(
            "chatmessage_set",
            queryset=ChatMessage.objects.select_related(
                "author",
                "author__user",
            ),
        ),
    )
)


def task_find_by_task_uuid(
    *, task_uuid: UUID, who: User, qs: Optional[TaskQuerySet] = None
) -> Optional[Task]:
    """Find a task given a user and uuid."""
    # Special care is needed, one can't write qs or Task.objects since that
    # would cause the given qs to be prematurely evaluated
    qs = Task.objects if qs is None else qs
    try:
        return qs.get(
            workspace_board_section__workspace_board__workspace__users=who,
            uuid=task_uuid,
        )
    except Task.DoesNotExist:
        return None
