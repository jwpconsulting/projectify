"""Workspace user services."""
from typing import Optional

from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

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


def workspace_user_delete(
    *,
    workspace_user: WorkspaceUser,
    who: User,
) -> None:
    """
    Delete a workspace user.

    Validate that own user can not be deleted.

    We do not support deleting one's own workspace user for now. This is
    to avoid that if a user is an admin, that they will leave the workspace
    inoperable.

    On the other hand, we might introduce a proper hand-off procedure,
    so big TODO maybe?
    """
    validate_perm("workspace.can_delete_workspace_user", who, workspace_user)
    if workspace_user.user == who:
        raise serializers.ValidationError(
            {"workspace_user": _("Can't delete own workspace user")}
        )
    workspace_user.delete()
