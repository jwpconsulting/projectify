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

from user.models import User
from workspace.models.task import Task
from workspace.models.workspace import Workspace
from workspace.models.workspace_board import WorkspaceBoard
from workspace.selectors.task import TaskDetailQuerySet, task_find_by_task_uuid
from workspace.selectors.workspace import workspace_find_by_workspace_uuid
from workspace.selectors.workspace_board import (
    workspace_board_find_by_workspace_board_uuid,
)
from workspace.serializers.task_detail import TaskDetailSerializer
from workspace.serializers.workspace import WorkspaceDetailSerializer
from workspace.serializers.workspace_board import (
    WorkspaceBoardDetailSerializer,
)
from workspace.types import ConsumerEvent, Message

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
        # TODO need to prefetch/select related here to avoid N+1
        workspace = workspace_find_by_workspace_uuid(
            who=self.user,
            workspace_uuid=self.uuid,
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
        # TODO prefetch / select related here
        workspace_board = workspace_board_find_by_workspace_board_uuid(
            who=self.user,
            workspace_board_uuid=self.uuid,
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
