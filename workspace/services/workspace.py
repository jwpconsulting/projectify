"""
Workspace services.

This is where all workspace related services will live in the future.
"""
from typing import Optional

from django.contrib.auth.models import (
    AbstractBaseUser,
)

from corporate.services.customer import customer_create
from projectify.utils import validate_perm
from user.models import User
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
    owner: User,
) -> Workspace:
    """Create a workspace."""
    # TODO validate that user can only create 1 unpaid workspace
    # TODO use Workspace.objects.create
    workspace = Workspace(title=title, description=description)
    workspace.save()
    workspace_add_user(workspace=workspace, user=owner, role="OWNER")
    customer_create(
        who=owner,
        workspace=workspace,
        # TODO not sure if this is good or not. Every workspace starts as a
        # trial workspace with 2 seats.
        seats=2,
    )
    return workspace


def workspace_update(
    *,
    workspace: Workspace,
    title: str,
    description: Optional[str] = None,
    who: User,
) -> Workspace:
    """Update a workspace."""
    validate_perm(
        "workspace.can_update_workspace",
        who,
        workspace,
    )
    workspace.title = title
    workspace.description = description
    workspace.save()
    return workspace


# TODO put in
# workspace/services/workspace_user_invite.py:workspace_user_invite_create
# TODO explicitly check authorization.
def workspace_add_user(
    *,
    workspace: Workspace,
    user: AbstractBaseUser,
    # TODO derive the correct role from an enum
    # Can we just use WorkspaceUserRoles here?
    role: str = "OBSERVER",
) -> WorkspaceUser:
    """Add user to workspace. Return new workspace user."""
    return workspace.workspaceuser_set.create(user=user, role=role)
