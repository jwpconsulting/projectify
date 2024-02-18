# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Copyright (C) 2022, 2023 JWP Consulting GK
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
Determine trial limit quota for workspace.

Limitations for trial plan:
Be able to create 10 boards and up to 100 sections across all boards
Be able to create 1000 tasks in that workspace
Be able to create 10 * 100 sub tasks
Be able to add one more user, therefore that workspace being limited to having
2 workspace users in total.
Be able to create 10 labels, assign them to all tasks

Limitations for a trial workspace are
- ChatMessage: 0 chat messages,
- Label: 10 labels
- SubTask: 1000 sub tasks,
- Task: 1000 tasks,
- TaskLabel: unlimited,
- WorkspaceBoard: 10,
- WorkspaceBoardSection: 100,
- WorkspaceUser + WorkspaceUserInivite(unredeemed): 2
"""
from dataclasses import dataclass
from typing import Literal, Optional, Union

from projectify.corporate.services.customer import (
    customer_check_active_for_workspace,
)
from projectify.workspace.models.chat_message import ChatMessage
from projectify.workspace.models.label import Label
from projectify.workspace.models.sub_task import SubTask
from projectify.workspace.models.task import Task
from projectify.workspace.models.task_label import TaskLabel
from projectify.workspace.models.workspace import Workspace
from projectify.workspace.models.workspace_board_section import (
    WorkspaceBoardSection,
)

Resource = Literal[
    "ChatMessage",
    "Label",
    "SubTask",
    "Task",
    "TaskLabel",
    "WorkspaceBoard",
    "WorkspaceBoardSection",
    "WorkspaceUserAndInvite",
]


Limitation = Union[None, int]
trial_conditions: dict[Resource, Limitation] = {
    "ChatMessage": 0,
    "Label": 10,
    "SubTask": 1000,
    "Task": 1000,
    "TaskLabel": None,
    "WorkspaceBoard": 10,
    "WorkspaceBoardSection": 100,
    "WorkspaceUserAndInvite": 2,
}


@dataclass(frozen=True, kw_only=True)
class Quota:
    """Store quota for a resource, including the maximum amount."""

    # None means irrelevant. No limit means counting unnecessary.
    current: Optional[int]
    # None means unlimited
    limit: Optional[int]
    within_quota: bool


def workspace_quota_for(*, resource: Resource, workspace: Workspace) -> Quota:
    """Return the quota within a workspace for a given resource."""
    limit: Optional[int]
    match customer_check_active_for_workspace(workspace=workspace):
        case "full":
            limit = None
        case "trial":
            limit = trial_conditions[resource]
        case "inactive":
            limit = 0
    # Short circuit for no limit
    if limit is None:
        return Quota(current=None, limit=None, within_quota=True)
    current: int
    match resource:
        case "ChatMessage":
            # XXX At the moment, chat messages are not supported
            current = ChatMessage.objects.filter(
                task__workspace=workspace
            ).count()
        case "Label":
            current = Label.objects.filter(workspace=workspace).count()
        case "SubTask":
            current = SubTask.objects.filter(task__workspace=workspace).count()
        case "Task":
            current = Task.objects.filter(
                workspace_board_section__workspace_board__workspace=workspace
            ).count()
        case "TaskLabel":
            current = TaskLabel.objects.filter(
                label__workspace=workspace
            ).count()
        case "WorkspaceBoard":
            current = workspace.workspaceboard_set.count()
        case "WorkspaceBoardSection":
            current = WorkspaceBoardSection.objects.filter(
                workspace_board__workspace=workspace
            ).count()
        case "WorkspaceUserAndInvite":
            user_count = workspace.users.count()
            invite_count = workspace.workspaceuserinvite_set.filter(
                redeemed=False
            ).count()
            current = user_count + invite_count
    return Quota(current=current, limit=limit, within_quota=current < limit)
