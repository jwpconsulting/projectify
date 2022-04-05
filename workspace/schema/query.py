"""Workspace schema."""
import uuid

import strawberry

from .. import (
    models,
)
from . import (
    types,
)


@strawberry.type
class Query:
    """Query."""

    @strawberry.field
    def workspaces(self, info) -> list[types.Workspace]:
        """Resolve user's workspaces."""
        return models.Workspace.objects.get_for_user(info.context.user)

    @strawberry.field
    def workspace(self, info, uuid: uuid.UUID) -> types.Workspace:
        """Resolve workspace by UUID."""
        return models.Workspace.objects.get_for_user_and_uuid(
            info.context.user,
            uuid,
        )

    @strawberry.field
    def workspace_board(self, info, uuid: uuid.UUID) -> types.WorkspaceBoard:
        """Resolve a specific workspace board."""
        return models.WorkspaceBoard.objects.get_for_user_and_uuid(
            info.context.user,
            uuid,
        )

    @strawberry.field
    def workspace_board_section(
        self, info, uuid: uuid.UUID
    ) -> types.WorkspaceBoardSection:
        """Resolve a workspace board section."""
        return models.WorkspaceBoardSection.objects.get_for_user_and_uuid(
            info.context.user,
            uuid,
        )

    @strawberry.field
    def task(self, info, uuid: uuid.UUID) -> types.Task:
        """Resolve a task."""
        return models.Task.objects.get_for_user_and_uuid(
            info.context.user,
            uuid,
        )

    @strawberry.field
    def sub_task(self, info, uuid: uuid.UUID) -> types.SubTask:
        """Resolve a sub task."""
        return models.SubTask.objects.get_for_user_and_uuid(
            info.context.user,
            uuid,
        )

    @strawberry.field
    def chat_message(self, info, uuid: uuid.UUID) -> types.ChatMessage:
        """Resolve a chat message."""
        return models.ChatMessage.objects.get_for_user_and_uuid(
            info.context.user,
            uuid,
        )
