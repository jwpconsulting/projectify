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

from ..models import TaskLabel
from ..models.chat_message import ChatMessage
from ..models.label import Label
from ..models.sub_task import SubTask
from ..models.task import Task
from ..models.workspace import Workspace
from ..models.workspace_board import WorkspaceBoard
from ..models.workspace_board_section import WorkspaceBoardSection
from ..models.workspace_user import WorkspaceUser
from ..types import ConsumerEvent

# TODO AsyncToSync is typed in a newer (unreleased) version of asgiref
# which we indirectly install with channels, which has not been
# renewed in a while Justus 2023-05-19
async_to_sync = cast(Any, _async_to_sync)

HasOrIsWorkspace = Union[
    Workspace,
    Label,
    WorkspaceUser,
    WorkspaceBoard,
]
HasOrIsWorkspaceBoard = Union[
    WorkspaceBoard,
    WorkspaceBoardSection,
    Task,
    TaskLabel,
    SubTask,
]
HasOrIsTask = Union[Task, TaskLabel, SubTask, ChatMessage]


def group_send(destination: str, event: ConsumerEvent) -> None:
    """Send message to a channels group."""
    channel_layer = get_channel_layer()
    if not channel_layer:
        raise Exception("Did not get channel layer")
    async_to_sync(channel_layer.group_send)(
        destination,
        event,
    )


# TODO accept workspace only
def send_workspace_change_signal(instance: HasOrIsWorkspace) -> None:
    """Send workspace.change signal to correct group."""
    match instance:
        case Workspace():
            workspace = instance
        case Label():
            workspace = instance.workspace
        case WorkspaceUser():
            workspace = instance.workspace
        case WorkspaceBoard():
            workspace = instance.workspace
    uuid = str(workspace.uuid)
    group_send(
        f"workspace-{uuid}",
        {
            "type": "workspace.change",
            "uuid": uuid,
        },
    )


# TODO accept workspace board only
def send_workspace_board_change_signal(
    instance: HasOrIsWorkspaceBoard,
) -> None:
    """Send workspace_board.change signal to correct group."""
    match instance:
        case WorkspaceBoard():
            workspace_board = instance
        case WorkspaceBoardSection():
            workspace_board = instance.workspace_board
        case Task():
            workspace_board = instance.workspace_board_section.workspace_board
        case TaskLabel():
            workspace_board = (
                instance.task.workspace_board_section.workspace_board
            )
        case SubTask():
            workspace_board = (
                instance.task.workspace_board_section.workspace_board
            )
    uuid = str(workspace_board.uuid)
    group_send(
        f"workspace-board-{uuid}",
        {
            "type": "workspace.board.change",
            "uuid": uuid,
        },
    )


# TODO accept task only
def send_task_change_signal(instance: HasOrIsTask) -> None:
    """Send task.change signal to correct group."""
    match instance:
        case Task():
            task = instance
        case TaskLabel():
            task = instance.task
        case SubTask():
            task = instance.task
        case ChatMessage():
            task = instance.task
    uuid = str(task.uuid)
    group_send(
        f"task-{uuid}",
        {
            "type": "task.change",
            "uuid": uuid,
        },
    )
