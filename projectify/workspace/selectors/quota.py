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

from django.db.models import Sum

from projectify.corporate.selectors.customer import (
    customer_check_active_for_workspace,
)
from projectify.lib.settings import get_settings
from projectify.workspace.types import Quota, WorkspaceQuota

from ..models import Task, Workspace

Resource = Literal["Task", "Project", "TeamMemberAndInvite", "Attachment"]

Limitation = Union[None, int]


class Limitations(TypedDict):
    """Contain all limitations."""

    Task: Limitation
    Project: Limitation
    TeamMemberAndInvite: Limitation
    Attachment: Limitation


trial_conditions: Limitations = {
    "Task": 1000,
    "Project": 10,
    "TeamMemberAndInvite": 2,
    # No attachments for trial
    "Attachment": 0,
}


# Full workspace conditions are somewhat like this:
# {
#     "Task": None,
#     "Project": None,
#     "TeamMemberAndInvite": workspace.customer.seats,
#     "Attachment": 100 * 1024 * 1024
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
    match customer_check_active_for_workspace(workspace=workspace):
        case "trial" | "inactive":
            return trial_conditions[resource]
        case "full":
            pass
    match resource:
        case "TeamMemberAndInvite":
            customer = workspace.customer
            return customer.seats
        case "Attachment":
            return 100 * 1024 * 1024
        case _:
            return None


def workspace_quota_for(*, resource: Resource, workspace: Workspace) -> Quota:
    """Return the quota within a workspace for a given resource."""
    limit = get_workspace_quota_for_resource(resource, workspace)
    # Short circuit for no limit
    if limit is None:
        return Quota(current=None, limit=None, can_create_more=True)
    match resource:
        case "Task":
            current = Task.objects.filter(project__workspace=workspace).count()
        case "Project":
            current = workspace.project_set.count()
        case "TeamMemberAndInvite":
            user_count = workspace.users.count()
            invite_count = workspace.teammemberinvite_set.filter(
                redeemed=False
            ).count()
            current = user_count + invite_count
        case "Attachment":
            aggregate = workspace.attachment_set.aggregate(
                total_size=Sum("size", default=0)
            )
            match aggregate:
                case {"total_size": int() as result}:
                    current = result
                case other:
                    raise RuntimeError(f"Unexpected result {other}")
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
        attachments=mk(resource="Attachment"),
    )
