"""Workspace board model tests."""
import pytest

from workspace.factory import WorkspaceUserFactory
from workspace.models.workspace import Workspace
from workspace.models.workspace_board import WorkspaceBoard
from workspace.models.workspace_user import WorkspaceUser
from workspace.services.workspace_board import workspace_board_archive
from workspace.services.workspace_board_section import (
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
        workspace: Workspace,
        workspace_board: WorkspaceBoard,
        workspace_user: WorkspaceUser,
    ) -> None:
        """Test that the workspace board is retrieved correctly."""
        WorkspaceUserFactory(
            workspace=workspace,
        )
        # The third user is other_workspace_user, the created of this board
        assert workspace_board.workspace.users.count() == 3
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

    def test_workspace(
        self,
        workspace: Workspace,
        workspace_board: WorkspaceBoard,
    ) -> None:
        """Test workspace property."""
        assert workspace_board.workspace == workspace
