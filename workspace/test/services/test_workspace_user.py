"""Test workspace user services."""
import pytest

from user.models import User
from workspace.models.workspace import Workspace
from workspace.models.workspace_user import WorkspaceUser
from workspace.services.workspace import workspace_add_user
from workspace.services.workspace_user import workspace_user_delete


@pytest.mark.django_db
def test_workspace_user_delete(
    workspace_user: WorkspaceUser,
    workspace: Workspace,
    unrelated_user: User,
) -> None:
    """Test deleting a workspace user after adding them."""
    count = workspace.users.count()
    new_workspace_user = workspace_add_user(
        workspace=workspace,
        # TODO perm check missing in workspace_add_user
        # E who=workspace_user.user,
        user=unrelated_user,
    )
    assert workspace.users.count() == count + 1
    workspace_user_delete(
        workspace_user=new_workspace_user, who=workspace_user.user
    )
    assert workspace.users.count() == count
