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
"""Workspace model selectors."""
from typing import Optional
from uuid import UUID

from django.db.models import Prefetch

from user.models import User
from workspace.models.workspace import Workspace, WorkspaceQuerySet
from workspace.models.workspace_board import WorkspaceBoard
from workspace.models.workspace_user import WorkspaceUser

WorkspaceDetailQuerySet = Workspace.objects.prefetch_related(
    "label_set",
).prefetch_related(
    Prefetch(
        "workspaceboard_set",
        queryset=WorkspaceBoard.objects.filter_by_archived(False),
    ),
    Prefetch(
        "workspaceuser_set",
        queryset=WorkspaceUser.objects.select_related(
            "user",
        ),
    ),
)

# 2023-11-30
# I am torn between requiring selectors to select for a user or not
# I don't want to accidentally leak data


def workspace_find_by_workspace_uuid(
    *,
    workspace_uuid: UUID,
    who: User,
    qs: Optional[WorkspaceQuerySet] = None,
) -> Optional[Workspace]:
    """Find a workspace by uuid for a given user."""
    if qs is None:
        qs = Workspace.objects.all()
    try:
        return qs.filter_for_user_and_uuid(user=who, uuid=workspace_uuid).get()
    except Workspace.DoesNotExist:
        return None
