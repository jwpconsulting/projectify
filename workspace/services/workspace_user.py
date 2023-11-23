"""Workspace user services."""


from typing import Optional

from projectify.utils import validate_perm
from user.models import User
from workspace.models.workspace_user import WorkspaceUser


def workspace_user_update(
    *,
    workspace_user: WorkspaceUser,
    who: User,
    job_title: Optional[str],
    # TODO should be an enum value
    role: str,
) -> WorkspaceUser:
    """Update a workspace user with new role and job title."""
    validate_perm("workspace.can_update_workspace_user", who, workspace_user)
    workspace_user.job_title = job_title
    workspace_user.role = role
    workspace_user.save()
    return workspace_user
