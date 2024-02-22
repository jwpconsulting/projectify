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

from projectify.workspace.services.workspace_board import (
    workspace_board_archive,
)

from ...models.workspace_board import WorkspaceBoard
from ...models.workspace_user import WorkspaceUser
from ...selectors.workspace_board import (
    workspace_board_find_by_workspace_board_uuid,
    workspace_board_find_by_workspace_uuid,
)

# So apparently this is also possible:
pytestmark = pytest.mark.django_db
# See https://docs.pytest.org/en/stable/example/markers.html#scoped-marking


def test_workspace_board_find_by_workspace_uuid(
    workspace_board: WorkspaceBoard,
    workspace_user: WorkspaceUser,
    unrelated_workspace_user: WorkspaceUser,
) -> None:
    """Test workspace_board_find_by_workspace_uuid."""
    qs = workspace_board_find_by_workspace_uuid(
        who=workspace_user.user,
        workspace_uuid=workspace_user.workspace.uuid,
    )
    assert qs.get() == workspace_board

    # Unrelated user can not access
    qs = workspace_board_find_by_workspace_uuid(
        who=unrelated_workspace_user.user,
        workspace_uuid=workspace_user.workspace.uuid,
    )
    assert qs.count() == 0

    # Filter by ONLY archived, and we will get nothing
    qs = workspace_board_find_by_workspace_uuid(
        who=workspace_user.user,
        workspace_uuid=workspace_user.workspace.uuid,
        archived=True,
    )
    assert qs.count() == 0


def test_workspace_board_find_by_workspace_board_uuid(
    workspace_board: WorkspaceBoard,
    workspace_user: WorkspaceUser,
    unrelated_workspace_user: WorkspaceUser,
    unrelated_workspace_board: WorkspaceBoard,
) -> None:
    """Test finding workspace board for a user by UUID."""
    # Normal case, user finds their workspace board
    assert workspace_board_find_by_workspace_board_uuid(
        workspace_board_uuid=workspace_board.uuid,
        who=workspace_user.user,
    )
    # Unrelated user finds their board
    assert workspace_board_find_by_workspace_board_uuid(
        workspace_board_uuid=unrelated_workspace_board.uuid,
        who=unrelated_workspace_user.user,
    )
    # Unrelated workspace user does not have access
    assert (
        workspace_board_find_by_workspace_board_uuid(
            workspace_board_uuid=workspace_board.uuid,
            who=unrelated_workspace_user.user,
        )
        is None
    )
    # And our user can not see unrelated user's board
    assert (
        workspace_board_find_by_workspace_board_uuid(
            workspace_board_uuid=unrelated_workspace_board.uuid,
            who=workspace_user.user,
        )
        is None
    )

    # Archiving hides it unless passing extra flag
    workspace_board_archive(
        who=workspace_user.user,
        workspace_board=workspace_board,
        archived=True,
    )
    assert (
        workspace_board_find_by_workspace_board_uuid(
            workspace_board_uuid=workspace_board.uuid,
            who=workspace_user.user,
        )
        is None
    )
    # Passing include_archived will make it show up again
    assert workspace_board_find_by_workspace_board_uuid(
        workspace_board_uuid=workspace_board.uuid,
        who=workspace_user.user,
        include_archived=True,
    )
