"""Workspace schema."""
import graphene
import graphene_django

from . import (
    models,
)


class Workspace(graphene_django.DjangoObjectType):
    """Workspace."""

    users = graphene.List("user.schema.User")
    boards = graphene.List("workspace.schema.WorkspaceBoard")

    def resolve_users(self, info):
        """Resolve workspace users."""
        return self.users.all()

    def resolve_boards(self, info):
        """Resolve workspace boards."""
        return self.workspaceboard_set.all()

    class Meta:
        """Meta."""

        fields = (
            "users",
            "created",
            "modified",
            "title",
            "description",
            "uuid",
        )
        model = models.Workspace


class WorkspaceBoard(graphene_django.DjangoObjectType):
    """WorkspaceBoard."""

    sections = graphene.List("workspace.schema.WorkspaceBoardSection")

    def resolve_sections(self, info):
        """Resolve workspace board sections."""
        return self.workspaceboardsection_set.all()

    class Meta:
        """Meta."""

        fields = ("created", "modified", "title", "description", "uuid")
        model = models.WorkspaceBoard


class WorkspaceBoardSection(graphene_django.DjangoObjectType):
    """WorkspaceBoardSection."""

    tasks = graphene.List("workspace.schema.Task")

    def resolve_tasks(self, info):
        """Resolve tasks for this workspace board section."""
        return self.task_set.all()

    class Meta:
        """Meta."""

        fields = ("created", "modified", "title", "description", "uuid")
        model = models.WorkspaceBoardSection


class Task(graphene_django.DjangoObjectType):
    """Task."""

    sub_tasks = graphene.List("workspace.schema.SubTask")

    def resolve_sub_tasks(self, info):
        """Resolve sub tasks for this task."""
        return self.subtask_set.all()

    class Meta:
        """Meta."""

        fields = ("created", "modified", "title", "description", "uuid")
        model = models.Task


class SubTask(graphene_django.DjangoObjectType):
    """SubTask."""

    class Meta:
        """Meta."""

        fields = ("created", "modified", "title", "description", "uuid")
        model = models.SubTask


class Query:
    """Query."""

    workspaces = graphene.List(Workspace)
    workspace_board = graphene.Field(WorkspaceBoard, uuid=graphene.ID())
    workspace_board_section = graphene.Field(
        WorkspaceBoardSection,
        uuid=graphene.ID(),
    )

    def resolve_workspaces(self, info):
        """Resolve user's workspaces."""
        return models.Workspace.objects.get_for_user(info.context.user)

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
