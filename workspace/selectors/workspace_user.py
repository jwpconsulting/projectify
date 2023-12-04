"""Workspace user selectors."""
from typing import Optional

from user.models import User
from workspace.models.workspace import Workspace
from workspace.models.workspace_user import WorkspaceUser


def workspace_user_find_for_workspace(
    *, user: User, workspace: Workspace
) -> Optional[WorkspaceUser]:
    """Find a workspace user."""
    try:
        return WorkspaceUser.objects.get(workspace=workspace, user=user)
    except WorkspaceUser.DoesNotExist:
        return None
