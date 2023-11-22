"""
Workspace app rules.

The order of rules follows the ordering of models.
"""
from typing import (
    Protocol,
)

from django.contrib.auth.models import (
    AbstractBaseUser,
)

import rules

from corporate import models as corporate_models

from . import (
    models,
)


class HasWorkspace(Protocol):
    """Workspace adjacent object that has .workspace."""

    @property
    def workspace(
        self,
    ) -> models.Workspace:
        """Return the workspace."""
        ...


# Role predicates
# Observer < Member < Maintainer < Owner
@rules.predicate
def is_at_least_observer(user: AbstractBaseUser, target: HasWorkspace) -> bool:
    """Return True if a user is at least an observer of workspace parent."""
    workspace = target.workspace
    try:
        workspace_user = (
            models.WorkspaceUser.objects.get_by_workspace_and_user(
                workspace,
                user,
            )
        )
    except models.WorkspaceUser.DoesNotExist:
        return False
    return workspace.has_at_least_role(
        workspace_user,
        models.WorkspaceUserRoles.OBSERVER,
    )


@rules.predicate
def is_at_least_member(user: AbstractBaseUser, target: HasWorkspace) -> bool:
    """Return True if a user is at least a member of workspace parent."""
    workspace = target.workspace
    try:
        workspace_user = (
            models.WorkspaceUser.objects.get_by_workspace_and_user(
                workspace,
                user,
            )
        )
    except models.WorkspaceUser.DoesNotExist:
        return False
    return workspace.has_at_least_role(
        workspace_user,
        models.WorkspaceUserRoles.MEMBER,
    )


@rules.predicate
def is_at_least_maintainer(
    user: AbstractBaseUser, target: HasWorkspace
) -> bool:
    """Return True if a user is at least a maintainer of workspace parent."""
    workspace = target.workspace
    try:
        workspace_user = (
            models.WorkspaceUser.objects.get_by_workspace_and_user(
                workspace,
                user,
            )
        )
    except models.WorkspaceUser.DoesNotExist:
        return False
    return workspace.has_at_least_role(
        workspace_user,
        models.WorkspaceUserRoles.MAINTAINER,
    )


@rules.predicate
def is_at_least_owner(user: AbstractBaseUser, target: HasWorkspace) -> bool:
    """Return True if a user is at least an owner of workspace parent."""
    workspace = target.workspace
    try:
        workspace_user = (
            models.WorkspaceUser.objects.get_by_workspace_and_user(
                workspace,
                user,
            )
        )
    except models.WorkspaceUser.DoesNotExist:
        return False
    return workspace.has_at_least_role(
        workspace_user,
        models.WorkspaceUserRoles.OWNER,
    )


@rules.predicate
def belongs_to_active_workspace(
    user: AbstractBaseUser, target: HasWorkspace
) -> bool:
    """
    Return True if target belongs to an active workspace.

    Also returns True if target is an active workspace itself.
    """
    workspace = target.workspace
    try:
        models.WorkspaceUser.objects.get_by_workspace_and_user(
            workspace,
            user,
        )
    except models.WorkspaceUser.DoesNotExist:
        return False
    try:
        customer: corporate_models.Customer = workspace.customer
    except corporate_models.Customer.DoesNotExist:
        return False
    return customer.active


# Workspace
# Anyone should be able to create a workspace
rules.add_perm(
    "workspace.can_create_workspace",
    is_at_least_owner,
)
rules.add_perm(
    "workspace.can_read_workspace",
    is_at_least_observer,
)
rules.add_perm(
    "workspace.can_update_workspace",
    is_at_least_owner,
)
rules.add_perm(
    "workspace.can_delete_workspace",
    is_at_least_owner,
)

# Workspace user invite
rules.add_perm(
    "workspace.can_create_workspace_user_invite",
    is_at_least_owner & belongs_to_active_workspace,
)
rules.add_perm(
    "workspace.can_read_workspace_user_invite",
    is_at_least_owner & belongs_to_active_workspace,
)
rules.add_perm(
    "workspace.can_update_workspace_user_invite",
    is_at_least_owner & belongs_to_active_workspace,
)
rules.add_perm(
    "workspace.can_delete_workspace_user_invite",
    is_at_least_owner & belongs_to_active_workspace,
)

# Workspace user
rules.add_perm(
    "workspace.can_create_workspace_user",
    is_at_least_owner & belongs_to_active_workspace,
)
rules.add_perm(
    "workspace.can_read_workspace_user",
    is_at_least_observer & belongs_to_active_workspace,
)
rules.add_perm(
    "workspace.can_update_workspace_user",
    is_at_least_owner & belongs_to_active_workspace,
)
rules.add_perm(
    "workspace.can_delete_workspace_user",
    is_at_least_owner & belongs_to_active_workspace,
)

# Workspace board
rules.add_perm(
    "workspace.can_create_workspace_board",
    is_at_least_maintainer & belongs_to_active_workspace,
)
rules.add_perm(
    "workspace.can_read_workspace_board",
    is_at_least_observer & belongs_to_active_workspace,
)
rules.add_perm(
    "workspace.can_update_workspace_board",
    is_at_least_maintainer & belongs_to_active_workspace,
)
rules.add_perm(
    "workspace.can_delete_workspace_board",
    is_at_least_maintainer & belongs_to_active_workspace,
)

# Workspace board section
rules.add_perm(
    "workspace.can_create_workspace_board_section",
    is_at_least_maintainer & belongs_to_active_workspace,
)
rules.add_perm(
    "workspace.can_read_workspace_board_section",
    is_at_least_observer & belongs_to_active_workspace,
)
rules.add_perm(
    "workspace.can_update_workspace_board_section",
    is_at_least_maintainer & belongs_to_active_workspace,
)
rules.add_perm(
    "workspace.can_delete_workspace_board_section",
    is_at_least_maintainer & belongs_to_active_workspace,
)

# Task
rules.add_perm(
    "workspace.can_create_task",
    is_at_least_member & belongs_to_active_workspace,
)
rules.add_perm(
    "workspace.can_read_task",
    is_at_least_observer & belongs_to_active_workspace,
)
rules.add_perm(
    "workspace.can_update_task",
    is_at_least_member & belongs_to_active_workspace,
)
rules.add_perm(
    "workspace.can_delete_task",
    is_at_least_maintainer & belongs_to_active_workspace,
)

# Label
rules.add_perm(
    "workspace.can_create_label",
    is_at_least_maintainer & belongs_to_active_workspace,
)
rules.add_perm(
    "workspace.can_read_label",
    is_at_least_observer & belongs_to_active_workspace,
)
rules.add_perm(
    "workspace.can_update_label",
    is_at_least_maintainer & belongs_to_active_workspace,
)
rules.add_perm(
    "workspace.can_delete_label",
    is_at_least_maintainer & belongs_to_active_workspace,
)

# Task label
rules.add_perm(
    "workspace.can_create_task_label",
    is_at_least_member & belongs_to_active_workspace,
)
rules.add_perm(
    "workspace.can_read_task_label",
    is_at_least_observer & belongs_to_active_workspace,
)
rules.add_perm(
    "workspace.can_update_task_label",
    is_at_least_member & belongs_to_active_workspace,
)
rules.add_perm(
    "workspace.can_delete_task_label",
    is_at_least_member & belongs_to_active_workspace,
)


# Sub task
rules.add_perm(
    "workspace.can_create_sub_task",
    is_at_least_member & belongs_to_active_workspace,
)
rules.add_perm(
    "workspace.can_read_sub_task",
    is_at_least_observer & belongs_to_active_workspace,
)
rules.add_perm(
    "workspace.can_update_sub_task",
    is_at_least_member & belongs_to_active_workspace,
)
rules.add_perm(
    "workspace.can_delete_sub_task",
    is_at_least_member & belongs_to_active_workspace,
)

# Chat message
rules.add_perm(
    "workspace.can_create_chat_message",
    is_at_least_member & belongs_to_active_workspace,
)
rules.add_perm(
    "workspace.can_read_chat_message",
    is_at_least_observer & belongs_to_active_workspace,
)
rules.add_perm(
    "workspace.can_update_chat_message",
    is_at_least_member & belongs_to_active_workspace,
)
rules.add_perm(
    "workspace.can_delete_chat_message",
    is_at_least_maintainer & belongs_to_active_workspace,
)
