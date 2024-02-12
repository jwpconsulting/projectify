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
"""Workspace board model tests."""
import pytest

from projectify.workspace.models.workspace import Workspace
from projectify.workspace.models.workspace_board import WorkspaceBoard
from projectify.workspace.models.workspace_user import WorkspaceUser
from projectify.workspace.services.workspace_board import (
    workspace_board_archive,
)
from projectify.workspace.services.workspace_board_section import (
    workspace_board_section_create,
)


@pytest.mark.django_db
class TestWorkspaceBoardManager:
    """Test WorkspaceBoard manager."""

    def test_filter_by_workspace(
        self,
        workspace: Workspace,
        workspace_board: WorkspaceBoard,
    ) -> None:
        """Test filter_by_workspace_uuid."""
        qs = WorkspaceBoard.objects.filter_by_workspace(workspace)
        assert list(qs) == [workspace_board]

    def test_filter_by_user(
        self,
        workspace_board: WorkspaceBoard,
        workspace_user: WorkspaceUser,
    ) -> None:
        """Test filter_by_user."""
        qs = WorkspaceBoard.objects.filter_by_user(workspace_user.user)
        assert list(qs) == [workspace_board]

    def test_filter_by_workspace_pks(
        self,
        workspace: Workspace,
        workspace_board: WorkspaceBoard,
    ) -> None:
        """Test filter_by_workspace_pks."""
        qs = WorkspaceBoard.objects.filter_by_workspace_pks(
            [workspace.pk],
        )
        assert list(qs) == [workspace_board]

    def test_filter_for_user_and_uuid(
        self,
        workspace_board: WorkspaceBoard,
        workspace_user: WorkspaceUser,
        # TODO what do these fixtures achieve?
        workspace: Workspace,
        other_workspace_user: WorkspaceUser,
    ) -> None:
        """Test that the workspace board is retrieved correctly."""
        assert workspace_board.workspace.users.count() == 2
        actual = WorkspaceBoard.objects.filter_for_user_and_uuid(
            workspace_user.user,
            workspace_board.uuid,
        )
        assert actual.get() == workspace_board

    def test_filter_by_archived(
        self, workspace_board: WorkspaceBoard, workspace_user: WorkspaceUser
    ) -> None:
        """Test filter_by_archived."""
        qs_archived = WorkspaceBoard.objects.filter_by_archived(True)
        qs_unarchived = WorkspaceBoard.objects.filter_by_archived(False)
        assert qs_archived.count() == 0
        assert qs_unarchived.count() == 1
        workspace_board_archive(
            workspace_board=workspace_board,
            who=workspace_user.user,
            archived=True,
        )
        assert qs_archived.count() == 1
        assert qs_unarchived.count() == 0
        workspace_board_archive(
            workspace_board=workspace_board,
            who=workspace_user.user,
            archived=False,
        )
        assert qs_archived.count() == 0
        assert qs_unarchived.count() == 1


@pytest.mark.django_db
class TestWorkspaceBoard:
    """Test WorkspaceBoard."""

    def test_factory(
        self,
        workspace: Workspace,
        workspace_board: WorkspaceBoard,
    ) -> None:
        """Test workspace board creation works."""
        assert workspace_board.workspace == workspace

    def test_add_workspace_board_section(
        self,
        workspace_board: WorkspaceBoard,
        workspace_user: WorkspaceUser,
    ) -> None:
        """Test workspace board section creation."""
        assert workspace_board.workspaceboardsection_set.count() == 0
        section = workspace_board_section_create(
            who=workspace_user.user,
            workspace_board=workspace_board,
            title="hello",
            description="world",
        )
        assert workspace_board.workspaceboardsection_set.count() == 1
        section2 = workspace_board_section_create(
            who=workspace_user.user,
            workspace_board=workspace_board,
            title="hello",
            description="world",
        )
        assert workspace_board.workspaceboardsection_set.count() == 2
        assert list(workspace_board.workspaceboardsection_set.all()) == [
            section,
            section2,
        ]
