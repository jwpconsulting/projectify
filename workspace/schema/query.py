"""Workspace schema."""
import graphene

from .. import (
    models,
)
from . import (
    types,
)


class Query:
    """Query."""

    workspaces = graphene.List(types.Workspace)
    workspace = graphene.Field(types.Workspace, uuid=graphene.ID())
    workspace_board = graphene.Field(types.WorkspaceBoard, uuid=graphene.ID())
    workspace_board_section = graphene.Field(
        types.WorkspaceBoardSection,
        uuid=graphene.ID(),
    )
    task = graphene.Field(types.Task, uuid=graphene.ID())
    sub_task = graphene.Field(types.SubTask, uuid=graphene.ID())

    def resolve_workspaces(self, info):
        """Resolve user's workspaces."""
        return models.Workspace.objects.get_for_user(info.context.user)

    def resolve_workspace(self, info, uuid):
        """Resolve workspace by UUID."""
        return models.Workspace.objects.get_for_user_and_uuid(
            info.context.user,
            uuid,
        )

    def resolve_workspace_board(self, info, uuid):
        """Resolve a specific workspace board."""
        return models.WorkspaceBoard.objects.get_for_user_and_uuid(
            info.context.user,
            uuid,
        )

    def resolve_workspace_board_section(self, info, uuid):
        """Resolve a workspace board section."""
        return models.WorkspaceBoardSection.objects.get_for_user_and_uuid(
            info.context.user,
            uuid,
        )

    def resolve_task(self, info, uuid):
        """Resolve a task."""
        return models.Task.objects.get_for_user_and_uuid(
            info.context.user,
            uuid,
        )

    def resolve_sub_task(self, info, uuid):
        """Resolve a sub task."""
        return models.SubTask.objects.get_for_user_and_uuid(
            info.context.user,
            uuid,
        )
