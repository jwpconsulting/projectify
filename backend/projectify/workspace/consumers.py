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
"""Workspace ws consumers."""
import logging
from typing import (
    Any,
    Literal,
    NotRequired,
    Type,
    TypedDict,
    TypeVar,
    cast,
)
from uuid import (
    UUID,
)

from django.db import models

from asgiref.sync import async_to_sync as _async_to_sync
from channels.generic.websocket import (
    JsonWebsocketConsumer,
)
from rest_framework import serializers, status

from projectify.user.models import User

from .models.project import Project
from .models.task import Task
from .models.workspace import Workspace
from .selectors.project import (
    ProjectDetailQuerySet,
    project_find_by_project_uuid,
)
from .selectors.quota import workspace_get_all_quotas
from .selectors.task import TaskDetailQuerySet, task_find_by_task_uuid
from .selectors.workspace import (
    WorkspaceDetailQuerySet,
    workspace_find_by_workspace_uuid,
)
from .serializers.project import ProjectDetailSerializer
from .serializers.task_detail import TaskDetailSerializer
from .serializers.workspace import WorkspaceDetailSerializer
from .types import ConsumerEvent

logger = logging.getLogger(__name__)

async_to_sync = cast(Any, _async_to_sync)


M = TypeVar("M", bound=models.Model)


def serialize(
    serializer: Type[serializers.ModelSerializer[M]],
    instance: M,
) -> object:
    """Serialize a django model instance and then render it to JSON."""
    return serializer(instance).data


def workspace_group_name(workspace: Workspace) -> str:
    """Return the channel layer group name for a workspace."""
    return f"workspace-{workspace.uuid}"


def project_group_name(project: Project) -> str:
    """Return the channel layer group name for a project."""
    return f"project-{project.uuid}"


def task_group_name(task: Task) -> str:
    """Return the channel layer group name for a task."""
    return f"task-{task.uuid}"


# The below duplications are clunky
class ClientRequest(TypedDict):
    """A message from a client to the ChangeConsumer."""

    action: Literal["subscribe", "unsubscribe"]
    resource: Literal["workspace", "project", "task"]
    uuid: UUID


class ClientRequestSerializer(serializers.Serializer):
    """Serializer for ClientRequest."""

    action = serializers.ChoiceField(choices=["subscribe", "unsubscribe"])
    resource = serializers.ChoiceField(
        choices=["workspace", "project", "task"]
    )
    uuid = serializers.UUIDField()


class ClientResponse(TypedDict):
    """An update to a resource."""

    kind: Literal["subscribed", "notSubscribed", "notFound", "changed", "gone"]
    resource: Literal["workspace", "project", "task"]
    uuid: UUID
    content: NotRequired[object]


class ClientResponseSerializer(serializers.Serializer):
    """Serializer for change."""

    kind = serializers.ChoiceField(
        choices=["subscribed", "notSubscribed", "notFound", "changed", "gone"]
    )
    resource = serializers.ChoiceField(
        choices=["workspace", "project", "task"]
    )
    uuid = serializers.UUIDField()
    content = serializers.DictField(required=False)


class ChangeConsumer(JsonWebsocketConsumer):
    """Allow subscribing to changes to workspace resources."""

    user: User
    workspace_subscriptions: dict[UUID, Workspace] = {}
    project_subscriptions: dict[UUID, Project] = {}
    task_subscriptions: dict[UUID, Task] = {}

    def connect(self) -> None:
        """Handle connect."""
        self.user = self.scope["user"]

        if self.user.is_anonymous:
            logger.debug("Anonymous user tried to connect")
            self.close(status.HTTP_403_FORBIDDEN)
            return

        self.accept()

    def add_subscription_for(
        self, resource: Literal["workspace", "project", "task"], uuid: UUID
    ) -> Literal["not_found", "ok"]:
        """Add a resource subscription."""
        match resource:
            case "workspace":
                workspace = workspace_find_by_workspace_uuid(
                    who=self.user, workspace_uuid=uuid
                )
                if workspace is None:
                    return "not_found"
                group_name = workspace_group_name(workspace)
                self.workspace_subscriptions[uuid] = workspace
            case "project":
                project = project_find_by_project_uuid(
                    who=self.user, project_uuid=uuid
                )
                if project is None:
                    return "not_found"
                group_name = project_group_name(project)
                self.project_subscriptions[uuid] = project
            case "task":
                task = task_find_by_task_uuid(who=self.user, task_uuid=uuid)
                if task is None:
                    return "not_found"
                group_name = task_group_name(task)
                self.task_subscriptions[uuid] = task
        async_to_sync(self.channel_layer.group_add)(
            group_name, self.channel_name
        )
        return "ok"

    def remove_subscription_for(
        self, resource: Literal["workspace", "project", "task"], uuid: UUID
    ) -> Literal["not_subscribed", "ok"]:
        """Remove a resource subscription."""
        match resource:
            case "workspace":
                workspace = self.workspace_subscriptions.get(uuid)
                if workspace is None:
                    return "not_subscribed"
                group_name = workspace_group_name(workspace)
            case "project":
                project = self.project_subscriptions.get(uuid)
                if project is None:
                    return "not_subscribed"
                group_name = project_group_name(project)
            case "task":
                task = self.task_subscriptions.get(uuid)
                if task is None:
                    return "not_subscribed"
                group_name = task_group_name(task)
        async_to_sync(self.channel_layer.group_discard)(
            group_name, self.channel_name
        )
        return "ok"

    def remove_all_subscriptions(self) -> None:
        """Remove all subscriptions, discard self from channel layer."""
        for u in self.workspace_subscriptions:
            self.remove_subscription_for("workspace", u)
        for u in self.project_subscriptions:
            self.remove_subscription_for("project", u)
        for u in self.task_subscriptions:
            self.remove_subscription_for("task", u)

    def disconnect(self, close_code: int) -> None:
        """Handle disconnect."""
        self.remove_all_subscriptions()
        logger.debug("Disconnecting with code %d", close_code)

    def respond(self, response: ClientResponse) -> None:
        """Respond to a client request."""
        serializer = ClientResponseSerializer(instance=response)
        self.send_json(serializer.data)

    def receive_json(self, content: Any) -> None:
        """Do nothing when receiving json."""
        serializer = ClientRequestSerializer(data=content)
        if not serializer.is_valid():
            self.close(status.HTTP_400_BAD_REQUEST)
            return
        data = cast(ClientRequest, serializer.validated_data)
        resource = data["resource"]
        uuid = data["uuid"]

        result: Literal["ok", "not_found", "not_subscribed"]

        match data["action"], resource:
            case "subscribe", resource:
                result = self.add_subscription_for(resource, uuid)
            case "unsubscribe", resource:
                result = self.remove_subscription_for(resource, uuid)

        match result:
            case "not_found":
                logger.debug(
                    "No object found for uuid %s and resource %s",
                    uuid,
                    resource,
                )
                self.respond(
                    {
                        "kind": "notFound",
                        "resource": resource,
                        "uuid": uuid,
                    }
                )
            case "not_subscribed":
                logger.debug(
                    "Not subscribed to uuid %s and resource %s", uuid, resource
                )
            case "ok":
                self.respond(
                    {
                        "kind": "subscribed",
                        "resource": resource,
                        "uuid": uuid,
                    }
                )
                pass

    def workspace_change(self, event: ConsumerEvent) -> None:
        """Respond to project change event."""
        # Check if already subscribed
        uuid = UUID(event["uuid"])
        workspace = self.workspace_subscriptions.get(uuid)
        if workspace is None:
            # This should be an error, probably...
            logger.warn("Couldn't find workspace for uuid %s", uuid)
            return
        workspace = workspace_find_by_workspace_uuid(
            who=self.user,
            workspace_uuid=workspace.uuid,
            qs=WorkspaceDetailQuerySet,
        )

        if workspace is None:
            self.respond(
                {
                    "kind": "gone",
                    "resource": "workspace",
                    "uuid": uuid,
                }
            )
            return

        workspace.quota = workspace_get_all_quotas(workspace)
        serialized = serialize(WorkspaceDetailSerializer, workspace)
        self.respond(
            {
                "kind": "changed",
                "resource": "workspace",
                "uuid": workspace.uuid,
                "content": serialized,
            }
        )

    def project_change(self, event: ConsumerEvent) -> None:
        """Respond to project change event."""
        uuid = UUID(event["uuid"])
        project = self.project_subscriptions.get(uuid)
        if project is None:
            # XXX This should be an error, probably
            logger.warn("Couldn't find project for uuid %s", uuid)
            return
        project = project_find_by_project_uuid(
            who=self.user, project_uuid=project.uuid, qs=ProjectDetailQuerySet
        )

        if project is None:
            self.respond(
                {
                    "kind": "gone",
                    "resource": "project",
                    "uuid": uuid,
                }
            )
            return

        serialized = serialize(ProjectDetailSerializer, project)
        self.respond(
            {
                "kind": "changed",
                "resource": "project",
                "uuid": project.uuid,
                "content": serialized,
            }
        )

    def task_change(self, event: ConsumerEvent) -> None:
        """Respond to project change event."""
        uuid = UUID(event["uuid"])
        task = self.task_subscriptions.get(uuid)
        if task is None:
            # XXX This should be an error, probably
            logger.warn("Couldn't find task for uuid %s", uuid)
            return
        task = task_find_by_task_uuid(
            who=self.user, task_uuid=task.uuid, qs=TaskDetailQuerySet
        )

        if task is None:
            self.respond(
                {
                    "kind": "gone",
                    "resource": "task",
                    "uuid": uuid,
                }
            )
            return

        serialized = serialize(TaskDetailSerializer, task)
        self.respond(
            {
                "kind": "changed",
                "resource": "task",
                "uuid": task.uuid,
                "content": serialized,
            }
        )
