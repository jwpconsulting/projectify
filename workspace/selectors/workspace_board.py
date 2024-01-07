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
"""Workspace board model selectors."""
from typing import Optional
from uuid import UUID

from user.models import User
from workspace.models.workspace_board import (
    WorkspaceBoard,
    WorkspaceBoardQuerySet,
)

WorkspaceBoardDetailQuerySet = WorkspaceBoard.objects.prefetch_related(
    "workspaceboardsection_set",
    "workspaceboardsection_set__task_set",
    "workspaceboardsection_set__task_set__assignee",
    "workspaceboardsection_set__task_set__assignee__user",
    "workspaceboardsection_set__task_set__labels",
    "workspaceboardsection_set__task_set__subtask_set",
).select_related(
    "workspace",
)


def workspace_board_find_by_workspace_uuid(
    *, workspace_uuid: UUID, who: User, archived: Optional[bool] = None
) -> WorkspaceBoardQuerySet:
    """Find workspace boards for a workspace."""
    qs = WorkspaceBoard.objects.filter_by_user(who)
    if archived is not None:
        qs = qs.filter_by_archived(archived)
    qs = qs.filter(workspace__uuid=workspace_uuid)
    return qs


def workspace_board_find_by_workspace_board_uuid(
    *,
    workspace_board_uuid: UUID,
    who: User,
    qs: Optional[WorkspaceBoardQuerySet] = None,
) -> Optional[WorkspaceBoard]:
    """Find a workspace by uuid for a given user."""
    qs = WorkspaceBoard.objects.all() if qs is None else qs
    try:
        return (
            qs.filter_for_user_and_uuid(user=who, uuid=workspace_board_uuid)
            .filter(archived__isnull=True)
            .get()
        )
    except WorkspaceBoard.DoesNotExist:
        return None
