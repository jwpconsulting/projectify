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
"""Workspace user selectors."""
from typing import Optional

from projectify.user.models import User
from projectify.workspace.models.workspace import Workspace
from projectify.workspace.models.workspace_user import WorkspaceUser


def workspace_user_find_for_workspace(
    *, user: User, workspace: Workspace
) -> Optional[WorkspaceUser]:
    """Find a workspace user."""
    try:
        return WorkspaceUser.objects.get(workspace=workspace, user=user)
    except WorkspaceUser.DoesNotExist:
        return None
