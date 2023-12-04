"""
Workspace app rules.

The order of rules follows the ordering of models.
"""
import logging
from typing import (
    Union,
)

import rules

from corporate.services.customer import customer_check_active_for_workspace
from corporate.types import WorkspaceFeatures
from user.models import User
from workspace.models.chat_message import ChatMessage
from workspace.models.const import WorkspaceUserRoles
from workspace.models.label import Label
from workspace.models.sub_task import SubTask
from workspace.models.task import Task
from workspace.models.task_label import TaskLabel
from workspace.models.workspace import Workspace
from workspace.models.workspace_board import WorkspaceBoard
from workspace.models.workspace_board_section import WorkspaceBoardSection
from workspace.models.workspace_user import WorkspaceUser
from workspace.models.workspace_user_invite import WorkspaceUserInvite
from workspace.selectors.workspace_user import (
    workspace_user_find_for_workspace,
)

logger = logging.getLogger(__name__)


WorkspaceTarget = Union[
    ChatMessage,
    Label,
    SubTask,
    Task,
    TaskLabel,
    Workspace,
    WorkspaceBoard,
    WorkspaceBoardSection,
    WorkspaceUser,
    WorkspaceUserInvite,
]


def get_workspace_from_target(target: WorkspaceTarget) -> Workspace:
    """Return a workspace."""
    match target:
        case Workspace():
            return target
        case WorkspaceBoardSection():
            return target.workspace_board.workspace
        case TaskLabel():
            return target.label.workspace
        case ChatMessage():
            return (
                target.task.workspace_board_section.workspace_board.workspace
            )
        case SubTask():
            return (
                target.task.workspace_board_section.workspace_board.workspace
            )
        case target:
            return target.workspace


def check_permissions_for(
    role: WorkspaceUserRoles, user: User, target: WorkspaceTarget
) -> bool:
    """Check whether a user has required role for target."""
    workspace = get_workspace_from_target(target)
    workspace_user = workspace_user_find_for_workspace(
        workspace=workspace,
        user=user,
    )
    if workspace_user is None:
        return False
    return workspace.has_at_least_role(workspace_user, role)


# Role predicates
# Observer < Member < Maintainer < Owner
@rules.predicate
def is_at_least_observer(user: User, target: WorkspaceTarget) -> bool:
    """Return True if a user is at least an observer of workspace parent."""
    return check_permissions_for(
        WorkspaceUserRoles.OBSERVER,
        user,
        target,
    )


@rules.predicate
def is_at_least_member(user: User, target: WorkspaceTarget) -> bool:
    """Return True if a user is at least a member of workspace parent."""
    return check_permissions_for(
        WorkspaceUserRoles.MEMBER,
        user,
        target,
    )


@rules.predicate
def is_at_least_maintainer(user: User, target: WorkspaceTarget) -> bool:
    """Return True if a user is at least a maintainer of workspace parent."""
    return check_permissions_for(
        WorkspaceUserRoles.MAINTAINER,
        user,
        target,
    )


@rules.predicate
def is_at_least_owner(user: User, target: WorkspaceTarget) -> bool:
    """Return True if a user is at least an owner of workspace parent."""
    return check_permissions_for(
        WorkspaceUserRoles.OWNER,
        user,
        target,
    )


# It is perhaps not necessary to check if the workspace exists,
# or we can cache it as part of the predicate invocation
def check_available_features(
    features: WorkspaceFeatures, user: User, target: WorkspaceTarget
) -> bool:
    """Return True if a workspace has a feature set active."""
    workspace = get_workspace_from_target(target)
    workspace_user = workspace_user_find_for_workspace(
        workspace=workspace,
        user=user,
    )
    if workspace_user is None:
        logger.warning("No workspace user found for user %s", user)
        return False
    return customer_check_active_for_workspace(workspace=workspace) == features


@rules.predicate
def belongs_to_full_workspace(user: User, target: WorkspaceTarget) -> bool:
    """
    Return True if target belongs to a full workspace.

    Also returns True if target is an active workspace itself.
    """
    return check_available_features("full", user, target)


@rules.predicate
def belongs_to_trial_workspace(user: User, target: WorkspaceTarget) -> bool:
    """Return True if target belongs to a workspace."""
    return check_available_features("trial", user, target)


# TODO rules should be of the format
# <app>.<action>_<resource>
# and not as currently
# <app>.can_<action>_<resource>
# Going here by the django-rules guide:
# https://github.com/dfunckt/django-rules#setting-up-rules

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

# Requirements for trial plan
# Be able to create 10 boards with 10 sections in each board
# Be able to to create 100 tasks in that workspace
# Be able to add one more user, therefore that workspace being limited to having
# 2 workspace users in total.
# Be able to create 10 labels

# Workspace user invite
rules.add_perm(
    "workspace.can_create_workspace_user_invite",
    is_at_least_owner & belongs_to_full_workspace,
)
rules.add_perm(
    "workspace.can_read_workspace_user_invite",
    is_at_least_owner & belongs_to_full_workspace,
)
rules.add_perm(
    "workspace.can_update_workspace_user_invite",
    is_at_least_owner & belongs_to_full_workspace,
)
rules.add_perm(
    "workspace.can_delete_workspace_user_invite",
    is_at_least_owner & belongs_to_full_workspace,
)

# Workspace user
rules.add_perm(
    "workspace.can_create_workspace_user",
    is_at_least_owner & belongs_to_full_workspace,
)
rules.add_perm(
    "workspace.can_read_workspace_user",
    is_at_least_observer & belongs_to_full_workspace,
)
rules.add_perm(
    "workspace.can_update_workspace_user",
    is_at_least_owner & belongs_to_full_workspace,
)
rules.add_perm(
    "workspace.can_delete_workspace_user",
    is_at_least_owner & belongs_to_full_workspace,
)

# Workspace board
rules.add_perm(
    "workspace.can_create_workspace_board",
    is_at_least_maintainer & belongs_to_full_workspace,
)
rules.add_perm(
    "workspace.can_read_workspace_board",
    is_at_least_observer & belongs_to_full_workspace,
)
rules.add_perm(
    "workspace.can_update_workspace_board",
    is_at_least_maintainer & belongs_to_full_workspace,
)
rules.add_perm(
    "workspace.can_delete_workspace_board",
    is_at_least_maintainer & belongs_to_full_workspace,
)

# Workspace board section
rules.add_perm(
    "workspace.can_create_workspace_board_section",
    is_at_least_maintainer & belongs_to_full_workspace,
)
rules.add_perm(
    "workspace.can_read_workspace_board_section",
    is_at_least_observer & belongs_to_full_workspace,
)
rules.add_perm(
    "workspace.can_update_workspace_board_section",
    is_at_least_maintainer & belongs_to_full_workspace,
)
rules.add_perm(
    "workspace.can_delete_workspace_board_section",
    is_at_least_maintainer & belongs_to_full_workspace,
)

# Task
rules.add_perm(
    "workspace.can_create_task",
    is_at_least_member & belongs_to_full_workspace,
)
rules.add_perm(
    "workspace.can_read_task",
    is_at_least_observer & belongs_to_full_workspace,
)
rules.add_perm(
    "workspace.can_update_task",
    is_at_least_member & belongs_to_full_workspace,
)
rules.add_perm(
    "workspace.can_delete_task",
    is_at_least_maintainer & belongs_to_full_workspace,
)

# Label
rules.add_perm(
    "workspace.can_create_label",
    is_at_least_maintainer & belongs_to_full_workspace,
)
rules.add_perm(
    "workspace.can_read_label",
    is_at_least_observer & belongs_to_full_workspace,
)
rules.add_perm(
    "workspace.can_update_label",
    is_at_least_maintainer & belongs_to_full_workspace,
)
rules.add_perm(
    "workspace.can_delete_label",
    is_at_least_maintainer & belongs_to_full_workspace,
)

# Task label
rules.add_perm(
    "workspace.can_create_task_label",
    is_at_least_member & belongs_to_full_workspace,
)
rules.add_perm(
    "workspace.can_read_task_label",
    is_at_least_observer & belongs_to_full_workspace,
)
rules.add_perm(
    "workspace.can_update_task_label",
    is_at_least_member & belongs_to_full_workspace,
)
rules.add_perm(
    "workspace.can_delete_task_label",
    is_at_least_member & belongs_to_full_workspace,
)


# Sub task
rules.add_perm(
    "workspace.can_create_sub_task",
    is_at_least_member & belongs_to_full_workspace,
)
rules.add_perm(
    "workspace.can_read_sub_task",
    is_at_least_observer & belongs_to_full_workspace,
)
rules.add_perm(
    "workspace.can_update_sub_task",
    is_at_least_member & belongs_to_full_workspace,
)
rules.add_perm(
    "workspace.can_delete_sub_task",
    is_at_least_member & belongs_to_full_workspace,
)

# Chat message
rules.add_perm(
    "workspace.can_create_chat_message",
    is_at_least_member & belongs_to_full_workspace,
)
rules.add_perm(
    "workspace.can_read_chat_message",
    is_at_least_observer & belongs_to_full_workspace,
)
rules.add_perm(
    "workspace.can_update_chat_message",
    is_at_least_member & belongs_to_full_workspace,
)
rules.add_perm(
    "workspace.can_delete_chat_message",
    is_at_least_maintainer & belongs_to_full_workspace,
)
