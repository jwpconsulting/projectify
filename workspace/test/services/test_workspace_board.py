"""Test workspace board services."""
import pytest

from workspace.models.workspace_board import WorkspaceBoard
from workspace.models.workspace_user import WorkspaceUser
from workspace.services.workspace_board import workspace_board_archive


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
