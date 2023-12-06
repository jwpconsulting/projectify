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
