"""
Workspace services.

This is where all workspace related services will live in the future.
"""
from typing import Optional

from django.contrib.auth.models import (
    AbstractBaseUser,
)

from workspace.models.workspace import (
    Workspace,
)
from workspace.models.workspace_user import (
    WorkspaceUser,
)


def workspace_create(
    *,
    title: str,
    description: Optional[str] = None,
    owner: Optional[AbstractBaseUser] = None,
) -> Workspace:
    """Create a workspace."""
    workspace = Workspace(title=title, description=description)
    workspace.save()
    if owner is not None:
        workspace_add_user(workspace=workspace, user=owner, role="OWNER")
    return workspace


def workspace_add_user(
    # TODO make *
    # TODO derive the correct role from an enum
    workspace: Workspace,
    user: AbstractBaseUser,
    role: str = "OBSERVER",
) -> WorkspaceUser:
    """Add user to workspace. Return new workspace user."""
    return workspace.workspaceuser_set.create(user=user, role=role)
