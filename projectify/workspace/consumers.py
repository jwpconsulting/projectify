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
from abc import (
    ABCMeta,
    abstractmethod,
)
from typing import (
    Any,
    Optional,
    Type,
    TypeVar,
    cast,
)
from uuid import (
    UUID,
)

from django.contrib.auth.models import (
    AbstractBaseUser,
)
from django.db import models

from asgiref.sync import async_to_sync as _async_to_sync
from channels.generic.websocket import (
    JsonWebsocketConsumer,
)
from rest_framework import serializers

from projectify.user.models import User
from projectify.workspace.models.task import Task
from projectify.workspace.models.workspace import Workspace
from projectify.workspace.models.workspace_board import WorkspaceBoard
from projectify.workspace.selectors.task import (
    TaskDetailQuerySet,
    task_find_by_task_uuid,
)
from projectify.workspace.selectors.workspace import (
    WorkspaceDetailQuerySet,
    workspace_find_by_workspace_uuid,
)
from projectify.workspace.selectors.workspace_board import (
    WorkspaceBoardDetailQuerySet,
    workspace_board_find_by_workspace_board_uuid,
)
from projectify.workspace.serializers.task_detail import TaskDetailSerializer
from projectify.workspace.serializers.workspace import (
    WorkspaceDetailSerializer,
)
from projectify.workspace.serializers.workspace_board import (
    WorkspaceBoardDetailSerializer,
)
from projectify.workspace.types import ConsumerEvent, Message

async_to_sync = cast(Any, _async_to_sync)


M = TypeVar("M", bound=models.Model)


def serialize(
    serializer: Type[serializers.ModelSerializer[M]],
    instance: Optional[M],
    event: ConsumerEvent,
) -> Message:
    """Serialize a django model instance and then render it to JSON."""
    return {
        "type": event["type"],
        "uuid": event["uuid"],
        # If the instance has been deleted, we return null / None
        "data": serializer(instance).data if instance else None,
    }


class BaseConsumer(JsonWebsocketConsumer, metaclass=ABCMeta):
    """Base class we use for all consumers below."""

    user: User
    uuid: UUID

    def connect(self) -> None:
        """Handle connect."""
        self.user = self.scope["user"]
        if self.user.is_anonymous:
            self.close(403)
            return
        self.uuid = self.scope["url_route"]["kwargs"]["uuid"]
        if self.get_object(self.user, self.uuid) is None:
            self.close(404)
            return
        self.accept()
        async_to_sync(self.channel_layer.group_add)(
            self.get_group_name(),
            self.channel_name,
        )

    def disconnect(self, close_code: object) -> None:
        """Handle disconnect."""
        async_to_sync(self.channel_layer.group_discard)(
            self.get_group_name(),
            self.channel_name,
        )

    def receive_json(self, content: object) -> None:
        """Do nothing when receiving json."""
        pass

    @abstractmethod
    def get_group_name(self) -> str:
        """Return the name used for this group."""
        ...

    @abstractmethod
    def get_object(self, user: User, uuid: UUID) -> Optional[object]:
        """Attempt getting the object to ensure the user has access to it."""
        ...


class WorkspaceConsumer(BaseConsumer):
    """Consumer for Workspace ws."""

    def get_group_name(self) -> str:
        """Return group name."""
        uuid = self.scope["url_route"]["kwargs"]["uuid"]
        return f"workspace-{uuid}"

    def get_object(self, user: User, uuid: UUID) -> Optional[Workspace]:
        """Find workspace belonging to this user."""
        return workspace_find_by_workspace_uuid(who=user, workspace_uuid=uuid)

    def workspace_change(self, event: ConsumerEvent) -> None:
        """Respond to workspace board change event."""
        workspace = workspace_find_by_workspace_uuid(
            who=self.user,
            workspace_uuid=self.uuid,
            qs=WorkspaceDetailQuerySet,
        )
        serialized = serialize(WorkspaceDetailSerializer, workspace, event)
        self.send_json(serialized)


class WorkspaceBoardConsumer(BaseConsumer):
    """Consumer for WorkspaceBoard ws."""

    def get_group_name(self) -> str:
        """Return group name."""
        uuid = self.scope["url_route"]["kwargs"]["uuid"]
        return f"workspace-board-{uuid}"

    def get_object(
        self, user: AbstractBaseUser, uuid: UUID
    ) -> Optional[WorkspaceBoard]:
        """Get workspace board."""
        try:
            return WorkspaceBoard.objects.filter_for_user_and_uuid(
                user, uuid
            ).get()
        except WorkspaceBoard.DoesNotExist:
            return None

    def workspace_board_change(self, event: ConsumerEvent) -> None:
        """Respond to workspace board change event."""
        workspace_board = workspace_board_find_by_workspace_board_uuid(
            who=self.user,
            workspace_board_uuid=self.uuid,
            qs=WorkspaceBoardDetailQuerySet,
        )
        serialized = serialize(
            WorkspaceBoardDetailSerializer, workspace_board, event
        )
        self.send_json(serialized)


class TaskConsumer(BaseConsumer):
    """Consumer for task ws events."""

    def get_group_name(self) -> str:
        """Return group name."""
        uuid = self.scope["url_route"]["kwargs"]["uuid"]
        return f"task-{uuid}"

    def get_object(self, user: User, uuid: UUID) -> Optional[Task]:
        """Get task."""
        return task_find_by_task_uuid(who=user, task_uuid=uuid)

    def task_change(self, event: ConsumerEvent) -> None:
        """Respond to workspace board change event."""
        task = task_find_by_task_uuid(
            who=self.user, task_uuid=self.uuid, qs=TaskDetailQuerySet
        )
        serialized = serialize(TaskDetailSerializer, task, event)
        self.send_json(serialized)
