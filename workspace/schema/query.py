"""Workspace schema."""
import uuid

from django.shortcuts import (
    get_object_or_404,
)

import strawberry

from graphql import (
    GraphQLResolveInfo,
)

from .. import (
    models,
)
from . import (
    types,
)


Info = GraphQLResolveInfo


@strawberry.type
class Query:
    """Query."""

    @strawberry.field
    def workspaces(self, info: Info) -> list[types.Workspace]:
        """Resolve user's workspaces."""
        return models.Workspace.objects.get_for_user(info.context.user)  # type: ignore

    @strawberry.field
    def workspace(self, info: Info, uuid: uuid.UUID) -> types.Workspace:
        """Resolve workspace by UUID."""
        qs = models.Workspace.objects.filter_for_user_and_uuid(
            info.context.user,
            uuid,
        )
        workspace = get_object_or_404(qs)
        return workspace  # type: ignore

    @strawberry.field
    def workspace_board(
        self, info: Info, uuid: uuid.UUID
    ) -> types.WorkspaceBoard:
        """Resolve a specific workspace board."""
        qs = models.WorkspaceBoard.objects.filter_for_user_and_uuid(
            info.context.user,
            uuid,
        )
        workspace_board = get_object_or_404(qs)
        return workspace_board  # type: ignore

    @strawberry.field
    def workspace_board_section(
        self, info: Info, uuid: uuid.UUID
    ) -> types.WorkspaceBoardSection:
        """Resolve a workspace board section."""
        qs = models.WorkspaceBoardSection.objects.filter_for_user_and_uuid(  # type: ignore
            info.context.user,
            uuid,
        )
        workspace_board_section = get_object_or_404(qs)
        return workspace_board_section  # type: ignore

    @strawberry.field
    def task(self, info: Info, uuid: uuid.UUID) -> types.Task:
        """Resolve a task."""
        qs = models.Task.objects.filter_for_user_and_uuid(
            info.context.user,
            uuid,
        )
        task = get_object_or_404(qs)
        return task  # type: ignore

    @strawberry.field
    def sub_task(self, info: Info, uuid: uuid.UUID) -> types.SubTask:
        """Resolve a sub task."""
        qs = models.SubTask.objects.filter_for_user_and_uuid(
            info.context.user,
            uuid,
        )
        sub_task = get_object_or_404(qs)
        return sub_task  # type: ignore

    @strawberry.field
    def chat_message(self, info: Info, uuid: uuid.UUID) -> types.ChatMessage:
        """Resolve a chat message."""
        qs = models.ChatMessage.objects.filter_for_user_and_uuid(
            info.context.user,
            uuid,
        )
        chat_message = get_object_or_404(qs)
        return chat_message  # type: ignore
