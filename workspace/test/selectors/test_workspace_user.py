"""Test workspace user selectors."""
import pytest

from user.models import User
from workspace.models.workspace import Workspace
from workspace.models.workspace_user import WorkspaceUser
from workspace.selectors.workspace_user import (
    workspace_user_find_for_workspace,
)


@pytest.mark.django_db
def test_workspace_user_find_for_workspace(
    workspace: Workspace,
    user: User,
    workspace_user: WorkspaceUser,
) -> None:
    """Test get_by_workspace_and_user."""
    assert (
        workspace_user_find_for_workspace(
            workspace=workspace,
            user=user,
        )
        == workspace_user
    )
