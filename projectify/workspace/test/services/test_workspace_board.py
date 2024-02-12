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
"""Test workspace board services."""
import pytest

from projectify.workspace.models.workspace_board import WorkspaceBoard
from projectify.workspace.models.workspace_user import WorkspaceUser
from projectify.workspace.services.workspace_board import (
    workspace_board_archive,
)


@pytest.mark.django_db
def test_archive(
    workspace_board: WorkspaceBoard, workspace_user: WorkspaceUser
) -> None:
    """Test archive method."""
    assert workspace_board.archived is None
    workspace_board_archive(
        workspace_board=workspace_board, archived=True, who=workspace_user.user
    )
    assert workspace_board.archived is not None


@pytest.mark.django_db
def test_unarchive(
    workspace_board: WorkspaceBoard, workspace_user: WorkspaceUser
) -> None:
    """Test unarchive method."""
    assert workspace_board.archived is None
    workspace_board_archive(
        workspace_board=workspace_board, archived=True, who=workspace_user.user
    )
    assert workspace_board.archived is not None
    workspace_board_archive(
        workspace_board=workspace_board,
        archived=False,
        who=workspace_user.user,
    )
    assert workspace_board.archived is None
