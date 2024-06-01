# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Copyright (C) 2024 JWP Consulting GK
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
"""Functions to handle signals."""
from typing import (
    Any,
    Union,
    cast,
)

from asgiref.sync import async_to_sync as _async_to_sync
from channels.layers import (
    get_channel_layer,
)

from ..models.label import Label
from ..models.project import Project
from ..models.task import Task
from ..models.team_member import TeamMember
from ..models.workspace import Workspace
from ..types import ConsumerEvent

# TODO AsyncToSync is typed in a newer (unreleased) version of asgiref
# which we indirectly install with channels, which has not been
# renewed in a while Justus 2023-05-19
async_to_sync = cast(Any, _async_to_sync)

HasOrIsWorkspace = Union[
    Workspace,
    Label,
    TeamMember,
    Project,
]


def group_send(destination: str, event: ConsumerEvent) -> None:
    """Send message to a channels group."""
    channel_layer = get_channel_layer()
    if not channel_layer:
        raise Exception("Did not get channel layer")
    async_to_sync(channel_layer.group_send)(
        destination,
        event,
    )


def send_workspace_change_signal(workspace: Workspace) -> None:
    """Send workspace.change signal to correct group."""
    uuid = str(workspace.uuid)
    group_send(
        f"workspace-{uuid}",
        {
            "type": "workspace.change",
            "uuid": uuid,
        },
    )


def send_project_change_signal(
    project: Project,
) -> None:
    """Send project.change signal to correct group."""
    uuid = str(project.uuid)
    group_send(
        f"project-{uuid}",
        {
            "type": "project.change",
            "uuid": uuid,
        },
    )


def send_task_change_signal(task: Task) -> None:
    """Send task.change signal to correct group."""
    uuid = str(task.uuid)
    group_send(
        f"task-{uuid}",
        {
            "type": "task.change",
            "uuid": uuid,
        },
    )
