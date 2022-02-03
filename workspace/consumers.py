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


class WorkspaceBoardConsumer(JsonWebsocketConsumer):
    """Consumer for WorkspaceBoard ws."""

    def connect(self):
        """Handle connect."""
        user = self.scope["user"]
        if user.is_anonymous:
            return
        self.accept()
        self.uuid = self.scope["url_route"]["kwargs"]["uuid"]
        self.group_name = f"workspace-board-{self.uuid}"
        models.WorkspaceBoard.objects.get_for_user_and_uuid(user, self.uuid)
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name,
        )

    def disconnect(self, close_code):
        """Handle disconnect."""
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name,
        )

    def receive_json(self, content):
        """Do nothing when receiving json."""
        pass

    def workspace_board_change(self, event):
        """Respond to workspace board change event."""
        event_uuid = event["instance"].uuid
        self.send_json(str(event_uuid))
