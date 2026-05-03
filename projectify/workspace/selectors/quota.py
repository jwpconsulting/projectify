# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2022, 2023 JWP Consulting GK
"""
Determine trial limit quota for workspace.

Limitations for a trial workspaces:
- Task: 1000 tasks,
- Project: 10,
- TeamMember + TeamMemberInivite(unredeemed): 2
"""

from functools import partial
from typing import Literal, TypedDict, Union

from projectify.corporate.selectors.customer import (
    customer_check_active_for_workspace,
)
from projectify.lib.settings import get_settings
from projectify.workspace.types import Quota, WorkspaceQuota

from ..models import Task, Workspace

Resource = Literal["Task", "Project", "TeamMemberAndInvite"]

Limitation = Union[None, int]


class Limitations(TypedDict):
    """Contain all limitations."""

    Task: Limitation
    Project: Limitation
    TeamMemberAndInvite: Limitation


trial_conditions: Limitations = {
    "Task": 1000,
    "Project": 10,
    "TeamMemberAndInvite": 2,
}

# Full workspace conditions are somewhat like this:
# {
#     "Task": None,
#     "Project": None,
#     "TeamMemberAndInvite": workspace.customer.seats,
# }


def get_workspace_quota_for_resource(
    resource: Resource, workspace: Workspace
) -> Limitation:
    """
    Get specific resource quota for a workspace.

    Return None if no limits exist or if Stripe integration isn't active.
    """
    if get_settings().STRIPE_CONFIG is None:
        return None
    status = customer_check_active_for_workspace(workspace=workspace)
    # We regard inactive as trial
    if status in ["trial", "inactive"]:
        return trial_conditions[resource]
    if resource == "TeamMemberAndInvite":
        customer = workspace.customer
        return customer.seats
    return None


def get_workspace_resource_count(
    resource: Resource, workspace: Workspace
) -> int:
    """Return resource count for a specific resource."""
    match resource:
        case "Task":
            return Task.objects.filter(project__workspace=workspace).count()
        case "Project":
            return workspace.project_set.count()
        case "TeamMemberAndInvite":
            user_count = workspace.users.count()
            invite_count = workspace.teammemberinvite_set.filter(
                redeemed=False
            ).count()
            return user_count + invite_count


def workspace_quota_for(*, resource: Resource, workspace: Workspace) -> Quota:
    """Return the quota within a workspace for a given resource."""
    limit = get_workspace_quota_for_resource(resource, workspace)
    # Short circuit for no limit
    if limit is None:
        return Quota(current=None, limit=None, can_create_more=True)
    current = get_workspace_resource_count(resource, workspace)
    return Quota(current=current, limit=limit, can_create_more=current < limit)


def workspace_get_all_quotas(workspace: Workspace) -> WorkspaceQuota:
    """Calculate all quotas for a workspace. Expensive calculation."""
    mk = partial(workspace_quota_for, workspace=workspace)
    return WorkspaceQuota(
        workspace_status=customer_check_active_for_workspace(
            workspace=workspace
        ),
        tasks=mk(resource="Task"),
        projects=mk(resource="Project"),
        team_members_and_invites=mk(resource="TeamMemberAndInvite"),
    )
