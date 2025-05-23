# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2022, 2023 JWP Consulting GK
"""
Determine trial limit quota for workspace.

Limitations for trial plan:
Be able to create 10 boards and up to 100 sections across all boards
Be able to create 1000 tasks in that workspace
Be able to create 10 * 100 sub tasks
Be able to add one more user, therefore that workspace being limited to having
2 team members in total.
Be able to create 10 labels, assign them to all tasks

Limitations for a trial workspace are
- ChatMessage: 0 chat messages,
- Label: 10 labels
- SubTask: 1000 sub tasks,
- Task: 1000 tasks,
- TaskLabel: unlimited,
- Project: 10,
- Section: 100,
- TeamMember + TeamMemberInivite(unredeemed): 2
"""

from functools import partial
from typing import Literal, TypedDict, Union

from projectify.corporate.selectors.customer import (
    customer_check_active_for_workspace,
)
from projectify.workspace.models.chat_message import ChatMessage
from projectify.workspace.models.label import Label
from projectify.workspace.models.section import Section
from projectify.workspace.models.sub_task import SubTask
from projectify.workspace.models.task import Task
from projectify.workspace.models.task_label import TaskLabel
from projectify.workspace.models.workspace import Workspace
from projectify.workspace.types import Quota, WorkspaceQuota

Resource = Literal[
    "ChatMessage",
    "Label",
    "SubTask",
    "Task",
    "TaskLabel",
    "Project",
    "Section",
    "TeamMemberAndInvite",
]

Limitation = Union[None, int]


class Limitations(TypedDict):
    """Contain all limitations."""

    ChatMessage: Limitation
    Label: Limitation
    SubTask: Limitation
    Task: Limitation
    TaskLabel: Limitation
    Project: Limitation
    Section: Limitation
    TeamMemberAndInvite: Limitation


trial_conditions: Limitations = {
    "ChatMessage": 0,
    "Label": 10,
    "SubTask": 1000,
    "Task": 1000,
    "TaskLabel": None,
    "Project": 10,
    "Section": 100,
    "TeamMemberAndInvite": 2,
}

# Full workspace conditions are somewhat like this:
# {
#     "ChatMessage": None,
#     "Label": None,
#     "SubTask": None,
#     "Task": None,
#     "TaskLabel": None,
#     "Project": None,
#     "Section": None,
#     "TeamMemberAndInvite": workspace.customer.seats,
# }


def get_workspace_quota_for_resource(
    resource: Resource, workspace: Workspace
) -> Limitation:
    """Get specific resource quota for a workspace."""
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
        case "ChatMessage":
            # XXX At the moment, chat messages are not supported
            return ChatMessage.objects.filter(
                task__workspace=workspace
            ).count()
        case "Label":
            return Label.objects.filter(workspace=workspace).count()
        case "SubTask":
            return SubTask.objects.filter(task__workspace=workspace).count()
        case "Task":
            return Task.objects.filter(
                section__project__workspace=workspace
            ).count()
        case "TaskLabel":
            return TaskLabel.objects.filter(label__workspace=workspace).count()
        case "Project":
            return workspace.project_set.count()
        case "Section":
            return Section.objects.filter(project__workspace=workspace).count()
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
        chat_messages=mk(resource="ChatMessage"),
        labels=mk(resource="Label"),
        sub_tasks=mk(resource="SubTask"),
        tasks=mk(resource="Task"),
        task_labels=mk(resource="TaskLabel"),
        projects=mk(resource="Project"),
        sections=mk(resource="Section"),
        team_members_and_invites=mk(resource="TeamMemberAndInvite"),
    )
