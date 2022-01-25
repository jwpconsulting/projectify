"""Workspace schema types."""
import graphene
import graphene_django

from .. import (
    models,
)
from . import (
    loader,
)


class Workspace(graphene_django.DjangoObjectType):
    """Workspace."""

    users = graphene.List("user.schema.User")
    boards = graphene.List("workspace.schema.types.WorkspaceBoard")

    def resolve_users(self, info):
        """Resolve workspace users."""
        return loader.workspace_user_loader.load(self.pk)

    def resolve_boards(self, info):
        """Resolve workspace boards."""
        return loader.workspace_workspace_board_loader.load(self.pk)

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

    sections = graphene.List("workspace.schema.types.WorkspaceBoardSection")

    def resolve_sections(self, info):
        """Resolve workspace board sections."""
        return loader.workspace_board_workspace_board_section_loader.load(
            self.pk,
        )

    class Meta:
        """Meta."""

        fields = ("created", "modified", "title", "description", "uuid")
        model = models.WorkspaceBoard


class WorkspaceBoardSection(graphene_django.DjangoObjectType):
    """WorkspaceBoardSection."""

    tasks = graphene.List("workspace.schema.types.Task")

    def resolve_tasks(self, info):
        """Resolve tasks for this workspace board section."""
        return self.task_set.all()

    class Meta:
        """Meta."""

        fields = ("created", "modified", "title", "description", "uuid")
        model = models.WorkspaceBoardSection


class Task(graphene_django.DjangoObjectType):
    """Task."""

    sub_tasks = graphene.List("workspace.schema.types.SubTask")

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
