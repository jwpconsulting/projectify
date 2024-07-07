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
    Optional,
    TypedDict,
    TypeVar,
    Union,
    cast,
)
from uuid import UUID

from django.db import models

from asgiref.sync import async_to_sync as _async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer
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
from .types import ConsumerEvent, Resource

logger = logging.getLogger(__name__)

async_to_sync = cast(Any, _async_to_sync)


M = TypeVar("M", bound=models.Model)


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

    kind: Literal[
        "subscribed",
        "unsubscribed",
        "already_subscribed",
        "not_subscribed",
        "not_found",
        "changed",
        "gone",
    ]
    resource: Literal["workspace", "project", "task"]
    uuid: UUID
    content: NotRequired[object]


class ClientResponseSerializer(serializers.Serializer):
    """Serializer for change."""

    kind = serializers.ChoiceField(
        choices=[
            "subscribed",
            "unsubscribed",
            "already_subscribed",
            "not_subscribed",
            "not_found",
            "changed",
            "gone",
        ]
    )
    resource = serializers.ChoiceField(
        choices=["workspace", "project", "task"]
    )
    uuid = serializers.UUIDField()
    content = serializers.DictField(required=False)


def get_group_name(resource: Resource, uuid: UUID) -> str:
    """Return the channel layer group name for a resource and uuid."""
    return f"{resource}-{uuid}"


ResourceInstance = Union[Workspace, Project, Task]


class ChangeConsumer(JsonWebsocketConsumer):
    """Allow subscribing to changes to workspace resources."""

    user: User
    subscriptions: dict[UUID, Union[Workspace, Project, Task]]

    def connect(self) -> None:
        """Handle connect."""
        self.subscriptions = {}

        self.user = self.scope["user"]

        if self.user.is_anonymous:
            logger.warning("Anonymous user tried to connect")
            self.close(status.HTTP_403_FORBIDDEN)
            return

        self.accept()

    def is_subscribed_to(self, resource: Resource, uuid: UUID) -> bool:
        """Return True if we are subscribed to a group."""
        sub = self.subscriptions.get(uuid)
        match resource, sub:
            case "workspace", Workspace():
                return True
            case "project", Project():
                return True
            case "task", Task():
                return True
            case _:
                return False

    T = TypeVar("T")

    def find_subscription(
        self, resource: Resource, uuid: UUID
    ) -> Optional[ResourceInstance]:
        """Return True if we are subscribed to a group."""
        sub = self.subscriptions.get(uuid)
        if sub is None:
            return None
        match resource, sub:
            case "workspace", Workspace():
                return sub
            case "project", Project():
                return sub
            case "task", Task():
                return sub
            case _:
                raise ValueError(
                    f"Type mismatch for sub {sub} with {uuid}, expected {resource}"
                )

    def pop_subscription(self, resource: Resource, uuid: UUID) -> None:
        """Pop a subscription, but only after type checking."""
        sub = self.find_subscription(resource, uuid)
        if sub is None:
            raise ValueError(
                f"Can't pop, what has not been subscribed: {resource} {uuid}"
            )
        self.subscriptions.pop(uuid)

    def add_subscription_for(
        self, resource: Resource, uuid: UUID
    ) -> Literal["not_found", "subscribed", "already_subscribed"]:
        """Add a resource subscription."""
        who = self.user
        inst: Optional[ResourceInstance]
        match resource, self.is_subscribed_to(resource, uuid):
            case "workspace", False:
                inst = workspace_find_by_workspace_uuid(
                    who=who, workspace_uuid=uuid
                )
            case "project", False:
                inst = project_find_by_project_uuid(who=who, project_uuid=uuid)
            case "task", False:
                inst = task_find_by_task_uuid(who=self.user, task_uuid=uuid)
            case _:
                return "already_subscribed"
        if inst is None:
            return "not_found"
        self.subscriptions[uuid] = inst
        async_to_sync(self.channel_layer.group_add)(
            get_group_name(resource, uuid), self.channel_name
        )
        return "subscribed"

    def remove_subscription_for(
        self, resource: Resource, uuid: UUID
    ) -> Literal["not_subscribed", "unsubscribed"]:
        """Remove a resource subscription."""
        if not self.is_subscribed_to(resource, uuid):
            return "not_subscribed"
        self.subscriptions.pop(uuid)
        async_to_sync(self.channel_layer.group_discard)(
            get_group_name(resource, uuid), self.channel_name
        )
        return "unsubscribed"

    def remove_all_subscriptions(self) -> None:
        """Remove all subscriptions, discard self from channel layer."""
        subs = list(self.subscriptions.items())
        for k, v in subs:
            match v:
                case Workspace():
                    self.remove_subscription_for("workspace", k)
                case Project():
                    self.remove_subscription_for("project", k)
                case Task():
                    self.remove_subscription_for("task", k)

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

        result: Literal[
            "subscribed",
            "not_found",
            "not_subscribed",
            "already_subscribed",
            "unsubscribed",
        ]

        match data["action"], resource:
            case "subscribe", resource:
                result = self.add_subscription_for(resource, uuid)
            case "unsubscribe", resource:
                result = self.remove_subscription_for(resource, uuid)

        response: ClientResponse

        match result:
            case "already_subscribed":
                logger.debug(
                    "Client was already subscribed to resource %s uuid %s",
                    resource,
                    uuid,
                )
                response = {
                    "kind": "already_subscribed",
                    "resource": resource,
                    "uuid": uuid,
                }
            case "not_found":
                logger.debug(
                    "No object found for uuid %s and resource %s",
                    uuid,
                    resource,
                )
                response = {
                    "kind": "not_found",
                    "resource": resource,
                    "uuid": uuid,
                }
            case "not_subscribed":
                logger.debug(
                    "Not subscribed to uuid %s and resource %s", uuid, resource
                )
                response = {
                    "kind": "not_subscribed",
                    "resource": resource,
                    "uuid": uuid,
                }
            case "unsubscribed":
                response = {
                    "kind": "unsubscribed",
                    "resource": resource,
                    "uuid": uuid,
                }
            case "subscribed":
                response = {
                    "kind": "subscribed",
                    "resource": resource,
                    "uuid": uuid,
                }
        self.respond(response)

    def change(self, event: ConsumerEvent) -> None:
        """Respond to project change event."""
        # Check if already subscribed
        uuid = UUID(event["uuid"])
        response: ClientResponse
        sub = self.find_subscription(event["resource"], uuid)
        result: Union[
            Literal["gone", "not_found", "never_subscribed"],
            serializers.Serializer,
        ]
        match event["kind"], sub:
            case "gone", _:
                result = "gone"
            case "changed", Workspace() as w:
                workspace = workspace_find_by_workspace_uuid(
                    who=self.user,
                    workspace_uuid=w.uuid,
                    qs=WorkspaceDetailQuerySet,
                )
                if workspace is not None:
                    workspace.quota = workspace_get_all_quotas(workspace)
                    result = WorkspaceDetailSerializer(workspace)
                else:
                    result = "not_found"
            case "changed", Project() as p:
                project = project_find_by_project_uuid(
                    who=self.user,
                    project_uuid=p.uuid,
                    qs=ProjectDetailQuerySet,
                )
                if project is not None:
                    result = ProjectDetailSerializer(project)
                else:
                    result = "not_found"
            case "changed", Task() as t:
                task = task_find_by_task_uuid(
                    who=self.user, task_uuid=t.uuid, qs=TaskDetailQuerySet
                )
                if task is not None:
                    result = TaskDetailSerializer(task)
                else:
                    result = "not_found"
            case "changed", None:
                result = "never_subscribed"

        match result:
            case "gone":
                self.remove_subscription_for(event["resource"], uuid)
                response = {
                    "kind": "gone",
                    "resource": event["resource"],
                    "uuid": uuid,
                }
            case "not_found":
                self.remove_subscription_for(event["resource"], uuid)
                response = {
                    "kind": "gone",
                    "resource": event["resource"],
                    "uuid": uuid,
                }
            case "never_subscribed":
                logger.warn(
                    "Received update for resource %s and uuid %s"
                    "despite never having subscribed",
                    event["resource"],
                    uuid,
                )
                return
            case _:
                response = {
                    "kind": "changed",
                    "resource": event["resource"],
                    "uuid": uuid,
                    "content": result.data,
                }
        self.respond(response)
