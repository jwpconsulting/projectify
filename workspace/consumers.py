"""Workspace ws consumers."""
from abc import (
    ABCMeta,
    abstractmethod,
)
from typing import (
    Any,
    cast,
)
from uuid import (
    UUID,
)

from django.contrib.auth.models import (
    AbstractBaseUser,
)

from asgiref.sync import async_to_sync as _async_to_sync
from channels.generic.websocket import (
    JsonWebsocketConsumer,
)

from . import (
    models,
    types,
)


async_to_sync = cast(Any, _async_to_sync)


class BaseConsumer(JsonWebsocketConsumer, metaclass=ABCMeta):
    """Base class we use for all consumers below."""

    def connect(self) -> None:
        """Handle connect."""
        user = self.scope["user"]
        if user.is_anonymous:
            return
        self.accept()
        uuid: UUID = self.scope["url_route"]["kwargs"]["uuid"]
        self.get_object(user, uuid)
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
    def get_object(self, user: AbstractBaseUser, uuid: UUID) -> None:
        """Attempt getting the object to ensure the user has access to it."""
        ...


class WorkspaceConsumer(BaseConsumer):
    """Consumer for Workspace ws."""

    def get_group_name(self) -> str:
        """Return group name."""
        uuid = self.scope["url_route"]["kwargs"]["uuid"]
        return f"workspace-{uuid}"

    def get_object(self, user: AbstractBaseUser, uuid: UUID) -> None:
        """Find workspace belonging to this user."""
        models.Workspace.objects.filter_for_user_and_uuid(user, uuid).get()

    def workspace_change(self, event: types.Message) -> None:
        """Respond to workspace board change event."""
        self.send_json(event)


class WorkspaceBoardConsumer(BaseConsumer):
    """Consumer for WorkspaceBoard ws."""

    def get_group_name(self) -> str:
        """Return group name."""
        uuid = self.scope["url_route"]["kwargs"]["uuid"]
        return f"workspace-board-{uuid}"

    def get_object(self, user: AbstractBaseUser, uuid: UUID) -> None:
        """Get workspace board."""
        models.WorkspaceBoard.objects.filter_for_user_and_uuid(
            user, uuid
        ).get()

    def workspace_board_change(self, event: types.Message) -> None:
        """Respond to workspace board change event."""
        self.send_json(event)


class TaskConsumer(BaseConsumer):
    """Consumer for task ws events."""

    def get_group_name(self) -> str:
        """Return group name."""
        uuid = self.scope["url_route"]["kwargs"]["uuid"]
        return f"task-{uuid}"

    def get_object(self, user: AbstractBaseUser, uuid: UUID) -> None:
        """Get task."""
        models.Task.objects.filter_for_user_and_uuid(user, uuid).get()

    def task_change(self, event: types.Message) -> None:
        """Respond to workspace board change event."""
        self.send_json(event)
