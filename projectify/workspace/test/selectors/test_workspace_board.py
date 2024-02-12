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
"""Test workspace board selectors."""
import pytest

from workspace.models.workspace_board import WorkspaceBoard
from workspace.models.workspace_user import WorkspaceUser
from workspace.selectors.workspace_board import (
    workspace_board_find_by_workspace_uuid,
)

# So apparently this is also possible:
pytestmark = pytest.mark.django_db
# See https://docs.pytest.org/en/stable/example/markers.html#scoped-marking


def test_workspace_board_find_by_workspace_uuid(
    workspace_board: WorkspaceBoard,
    workspace_user: WorkspaceUser,
) -> None:
    """Test workspace_board_find_by_workspace_uuid."""
    qs = workspace_board_find_by_workspace_uuid(
        who=workspace_user.user,
        workspace_uuid=workspace_user.workspace.uuid,
    )
    assert qs.get() == workspace_board
    qs = workspace_board_find_by_workspace_uuid(
        who=workspace_user.user,
        workspace_uuid=workspace_user.workspace.uuid,
        archived=True,
    )
    assert qs.count() == 0
