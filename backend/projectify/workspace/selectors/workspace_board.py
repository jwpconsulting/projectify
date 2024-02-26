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

from django.db.models import QuerySet

from projectify.user.models import User

from ..models.workspace_board import WorkspaceBoard

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
) -> QuerySet[WorkspaceBoard]:
    """Find workspace boards for a workspace."""
    qs = WorkspaceBoard.objects.filter(
        workspace__users=who, workspace__uuid=workspace_uuid
    )
    if archived is not None:
        qs = qs.filter(archived__isnull=not archived)
    return qs


def workspace_board_find_by_workspace_board_uuid(
    *,
    workspace_board_uuid: UUID,
    who: User,
    qs: Optional[QuerySet[WorkspaceBoard]] = None,
    archived: bool = False,
) -> Optional[WorkspaceBoard]:
    """Find a workspace by uuid for a given user."""
    qs = WorkspaceBoard.objects.all() if qs is None else qs
    qs = qs.filter(archived__isnull=not archived)
    qs = qs.filter(workspace__users=who, uuid=workspace_board_uuid)
    try:
        return qs.get()
    except WorkspaceBoard.DoesNotExist:
        return None
