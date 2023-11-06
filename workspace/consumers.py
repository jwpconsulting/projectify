"""Workspace ws consumers."""
from abc import (
    ABCMeta,
    abstractmethod,
)
from typing import (
    Any,
    Optional,
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
            self.close(403)
            return
        uuid: UUID = self.scope["url_route"]["kwargs"]["uuid"]
        if self.get_object(user, uuid) is None:
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
    def get_object(
        self, user: AbstractBaseUser, uuid: UUID
    ) -> Optional[object]:
        """Attempt getting the object to ensure the user has access to it."""
        ...


class WorkspaceConsumer(BaseConsumer):
    """Consumer for Workspace ws."""

    def get_group_name(self) -> str:
        """Return group name."""
        uuid = self.scope["url_route"]["kwargs"]["uuid"]
        return f"workspace-{uuid}"

    def get_object(
        self, user: AbstractBaseUser, uuid: UUID
    ) -> Optional[models.Workspace]:
        """Find workspace belonging to this user."""
        try:
            return models.Workspace.objects.filter_for_user_and_uuid(
                user, uuid
            ).get()
        except models.Workspace.DoesNotExist:
            return None

    def workspace_change(self, event: types.Message) -> None:
        """Respond to workspace board change event."""
        self.send_json(event)


class WorkspaceBoardConsumer(BaseConsumer):
    """Consumer for WorkspaceBoard ws."""

    def get_group_name(self) -> str:
        """Return group name."""
        uuid = self.scope["url_route"]["kwargs"]["uuid"]
        return f"workspace-board-{uuid}"

    def get_object(
        self, user: AbstractBaseUser, uuid: UUID
    ) -> Optional[models.WorkspaceBoard]:
        """Get workspace board."""
        try:
            return models.WorkspaceBoard.objects.filter_for_user_and_uuid(
                user, uuid
            ).get()
        except models.WorkspaceBoard.DoesNotExist:
            return None

    def workspace_board_change(self, event: types.Message) -> None:
        """Respond to workspace board change event."""
        self.send_json(event)


class TaskConsumer(BaseConsumer):
    """Consumer for task ws events."""

    def get_group_name(self) -> str:
        """Return group name."""
        uuid = self.scope["url_route"]["kwargs"]["uuid"]
        return f"task-{uuid}"

    def get_object(
        self, user: AbstractBaseUser, uuid: UUID
    ) -> Optional[models.Task]:
        """Get task."""
        try:
            return models.Task.objects.filter_for_user_and_uuid(
                user, uuid
            ).get()
        except models.Task.DoesNotExist:
            return None

    def task_change(self, event: types.Message) -> None:
        """Respond to workspace board change event."""
        self.send_json(event)
