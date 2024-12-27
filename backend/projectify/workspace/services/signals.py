# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2024 JWP Consulting GK
"""Functions to handle signals."""

from typing import Any, Literal, Union, cast

from asgiref.sync import async_to_sync as _async_to_sync
from channels.layers import get_channel_layer

from ..models.project import Project
from ..models.task import Task
from ..models.workspace import Workspace
from ..types import ConsumerEvent, Resource

# TODO AsyncToSync is typed in a newer (unreleased) version of asgiref
# which we indirectly install with channels, which has not been
# renewed in a while Justus 2023-05-19
async_to_sync = cast(Any, _async_to_sync)


def send_change_signal(
    kind: Literal["changed", "gone"], object: Union[Workspace, Project, Task]
) -> None:
    """Send a change signal to the correct channels layer group."""
    resource: Resource
    match object:
        case Workspace():
            group = f"workspace-{object.uuid}"
            resource = "workspace"
        case Project():
            group = f"project-{object.uuid}"
            resource = "project"
        case Task():
            group = f"task-{object.uuid}"
            resource = "task"
    event: ConsumerEvent = {
        "type": "change",
        "resource": resource,
        "uuid": str(object.uuid),
        "kind": kind,
    }
    channel_layer = get_channel_layer()
    if not channel_layer:
        raise Exception("Did not get channel layer")
    async_to_sync(channel_layer.group_send)(group, event)
