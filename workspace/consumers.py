"""Workspace ws consumers."""
from asgiref.sync import (
    async_to_sync,
)
from channels.generic.websocket import (
    JsonWebsocketConsumer,
)

from . import (
    models,
)


class WorkspaceConsumer(JsonWebsocketConsumer):
    """Consumer for Workspace ws."""

    def get_group_name(self):
        """Return group name."""
        uuid = self.scope["url_route"]["kwargs"]["uuid"]
        return f"workspace-{uuid}"

    def connect(self):
        """Handle connect."""
        user = self.scope["user"]
        if user.is_anonymous:
            return
        self.accept()
        uuid = self.scope["url_route"]["kwargs"]["uuid"]
        models.Workspace.objects.get_for_user_and_uuid(user, uuid)
        async_to_sync(self.channel_layer.group_add)(
            self.get_group_name(),
            self.channel_name,
        )

    def disconnect(self, close_code):
        """Handle disconnect."""
        async_to_sync(self.channel_layer.group_discard)(
            self.get_group_name(),
            self.channel_name,
        )

    def receive_json(self, content):
        """Do nothing when receiving json."""
        pass

    def workspace_change(self, event):
        """Respond to workspace board change event."""
        event_uuid = event["uuid"]
        self.send_json(str(event_uuid))


class WorkspaceBoardConsumer(JsonWebsocketConsumer):
    """Consumer for WorkspaceBoard ws."""

    def get_group_name(self):
        """Return group name."""
        uuid = self.scope["url_route"]["kwargs"]["uuid"]
        return f"workspace-board-{uuid}"

    def connect(self):
        """Handle connect."""
        user = self.scope["user"]
        if user.is_anonymous:
            return
        self.accept()
        uuid = self.scope["url_route"]["kwargs"]["uuid"]
        models.WorkspaceBoard.objects.get_for_user_and_uuid(user, uuid)
        async_to_sync(self.channel_layer.group_add)(
            self.get_group_name(),
            self.channel_name,
        )

    def disconnect(self, close_code):
        """Handle disconnect."""
        async_to_sync(self.channel_layer.group_discard)(
            self.get_group_name(),
            self.channel_name,
        )

    def receive_json(self, content):
        """Do nothing when receiving json."""
        pass

    def workspace_board_change(self, event):
        """Respond to workspace board change event."""
        event_uuid = event["uuid"]
        self.send_json(str(event_uuid))


class TaskConsumer(JsonWebsocketConsumer):
    """Consumer for task ws events."""

    def get_group_name(self):
        """Return group name."""
        uuid = self.scope["url_route"]["kwargs"]["uuid"]
        return f"task-{uuid}"

    def connect(self):
        """Handle connect."""
        user = self.scope["user"]
        if user.is_anonymous:
            return
        self.accept()
        uuid = self.scope["url_route"]["kwargs"]["uuid"]
        models.Task.objects.get_for_user_and_uuid(user, uuid)
        async_to_sync(self.channel_layer.group_add)(
            self.get_group_name(),
            self.channel_name,
        )

    def disconnect(self, close_code):
        """Handle disconnect."""
        async_to_sync(self.channel_layer.group_discard)(
            self.get_group_name(),
            self.channel_name,
        )

    def receive_json(self, content):
        """Do nothing when receiving json."""
        pass

    def task_change(self, event):
        """Respond to workspace board change event."""
        event_uuid = event["uuid"]
        self.send_json(str(event_uuid))
