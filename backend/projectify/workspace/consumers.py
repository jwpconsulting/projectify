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
from .types import ConsumerEvent, Message

logger = logging.getLogger(__name__)

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
            self.close(status.HTTP_403_FORBIDDEN)
            return
        self.uuid = self.scope["url_route"]["kwargs"]["uuid"]
        if self.get_object(self.user, self.uuid) is None:
            self.close(status.HTTP_404_NOT_FOUND)
            return
        self.accept()
        async_to_sync(self.channel_layer.group_add)(
            self.get_group_name(),
            self.channel_name,
        )

    def disconnect(self, close_code: int) -> None:
        """Handle disconnect."""
        async_to_sync(self.channel_layer.group_discard)(
            self.get_group_name(),
            self.channel_name,
        )
        logger.debug("Disconnecting with code %d", close_code)

    def receive_json(self, content: object) -> None:
        """Do nothing when receiving json."""
        del content
        logger.debug("Received message, but don't know what to do with it.")

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
        """Respond to project change event."""
        workspace = workspace_find_by_workspace_uuid(
            who=self.user,
            workspace_uuid=self.uuid,
            qs=WorkspaceDetailQuerySet,
        )

        if workspace is None:
            self.disconnect(close_code=status.HTTP_410_GONE)
            return

        workspace.quota = workspace_get_all_quotas(workspace)
        serialized = serialize(WorkspaceDetailSerializer, workspace, event)
        self.send_json(serialized)


class ProjectConsumer(BaseConsumer):
    """Consumer for Project ws."""

    def get_group_name(self) -> str:
        """Return group name."""
        uuid = self.scope["url_route"]["kwargs"]["uuid"]
        return f"project-{uuid}"

    def get_object(self, user: User, uuid: UUID) -> Optional[Project]:
        """Get project."""
        return project_find_by_project_uuid(
            project_uuid=uuid,
            who=user,
        )

    def project_change(self, event: ConsumerEvent) -> None:
        """Respond to project change event."""
        project = project_find_by_project_uuid(
            who=self.user,
            project_uuid=self.uuid,
            qs=ProjectDetailQuerySet,
        )

        if project is None:
            self.disconnect(close_code=status.HTTP_410_GONE)
            return

        serialized = serialize(ProjectDetailSerializer, project, event)
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
        """Respond to project change event."""
        task = task_find_by_task_uuid(
            who=self.user, task_uuid=self.uuid, qs=TaskDetailQuerySet
        )

        if task is None:
            self.disconnect(close_code=status.HTTP_410_GONE)
            return

        serialized = serialize(TaskDetailSerializer, task, event)
        self.send_json(serialized)
