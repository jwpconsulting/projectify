"""Workspace schema types."""
import graphene
import graphene_django

from .. import (
    models,
)


class Workspace(graphene_django.DjangoObjectType):
    """Workspace."""

    users = graphene.List("user.schema.types.User")
    boards = graphene.List("workspace.schema.types.WorkspaceBoard")
    archived_boards = graphene.List("workspace.schema.types.WorkspaceBoard")
    labels = graphene.List("workspace.schema.types.Label")
    picture = graphene.String()

    def resolve_users(self, info):
        """Resolve workspace users."""
        return info.context.loader.workspace_user_loader.load(self.pk)

    def resolve_boards(self, info):
        """Resolve workspace boards."""
        return info.context.loader.workspace_workspace_board_loader.load(
            self.pk
        )

    def resolve_archived_boards(self, info):
        """Resolve archived workspace boards."""
        loader = info.context.loader.workspace_archived_workspace_board_loader
        return loader.load(self.pk)

    def resolve_labels(self, info):
        """Resolve labels."""
        loader = info.context.loader.workspace_label_loader
        return loader.load(self.pk)

    def resolve_picture(self, info):
        """Resolve picture."""
        if self.picture:
            return self.picture.url

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
    workspace = graphene.Field("workspace.schema.types.Workspace")

    def resolve_sections(self, info):
        """Resolve workspace board sections."""
        loader = info.context.loader
        return loader.workspace_board_workspace_board_section_loader.load(
            self.pk,
        )

    def resolve_workspace(self, info):
        """Resolve workspace."""
        return info.context.loader.workspace_loader.load(self.workspace.pk)

    class Meta:
        """Meta."""

        fields = (
            "created",
            "modified",
            "title",
            "description",
            "uuid",
            "archived",
            "deadline",
        )
        model = models.WorkspaceBoard


class WorkspaceBoardSection(graphene_django.DjangoObjectType):
    """WorkspaceBoardSection."""

    tasks = graphene.List("workspace.schema.types.Task")
    workspace_board = graphene.Field("workspace.schema.types.WorkspaceBoard")

    def resolve_tasks(self, info):
        """Resolve tasks for this workspace board section."""
        return info.context.loader.workspace_board_section_task_loader.load(
            self.pk
        )

    def resolve_workspace_board(self, info):
        """Resolve workspace board."""
        return info.context.loader.workspace_board_loader.load(
            self.workspace_board.pk
        )

    class Meta:
        """Meta."""

        fields = (
            "created",
            "modified",
            "title",
            "description",
            "uuid",
            "order",
        )
        model = models.WorkspaceBoardSection


class Task(graphene_django.DjangoObjectType):
    """Task."""

    sub_tasks = graphene.List("workspace.schema.types.SubTask")
    chat_messages = graphene.List("workspace.schema.types.ChatMessage")
    workspace_board_section = graphene.Field(
        "workspace.schema.types.WorkspaceBoardSection",
    )
    next_workspace_board_section = graphene.Field(
        "workspace.schema.types.WorkspaceBoardSection",
    )
    labels = graphene.List("workspace.schema.types.Label")

    def resolve_sub_tasks(self, info):
        """Resolve sub tasks for this task."""
        return info.context.loader.task_sub_task_loader.load(self.pk)

    def resolve_chat_messages(self, info):
        """Resolve chat messages for this task."""
        return info.context.loader.task_chat_message_loader.load(self.pk)

    def resolve_workspace_board_section(self, info):
        """Resolve workspace board section for this task."""
        return info.context.loader.workspace_board_section_loader.load(
            self.workspace_board_section.pk,
        )

    def resolve_next_workspace_board_section(self, info):
        """Resolve the next section."""
        section = self.get_next_section()
        if section:
            return info.context.loader.workspace_board_section_loader.load(
                section.pk,
            )

    def resolve_labels(self, info):
        """Resolve labels for this task."""
        return info.context.loader.task_task_label_loader.load(self.pk)

    class Meta:
        """Meta."""

        fields = (
            "created",
            "modified",
            "title",
            "description",
            "uuid",
            "order",
            "assignee",
        )
        model = models.Task


class Label(graphene_django.DjangoObjectType):
    """Label."""

    def resolve_workspace(self, info):
        """Resolve workspace."""
        return info.context.loader.workspace_loader.load(self.workspace.pk)

    class Meta:
        """Meta."""

        fields = (
            "name",
            "color",
            "workspace",
            "uuid",
        )
        model = models.Label


class SubTask(graphene_django.DjangoObjectType):
    """SubTask."""

    def resolve_task(self, info):
        """Resolve task with data loader."""
        return info.context.loader.task_loader.load(self.task.pk)

    class Meta:
        """Meta."""

        fields = (
            "created",
            "modified",
            "title",
            "description",
            "uuid",
            "order",
            "task",
            "done",
        )
        model = models.SubTask


class ChatMessage(graphene_django.DjangoObjectType):
    """ChatMessage."""

    def resolve_author(self, info):
        """Resolve author."""
        return info.context.loader.user_loader.load(self.author.pk)

    class Meta:
        """Meta."""

        fields = (
            "created",
            "modified",
            "uuid",
            "text",
            "author",
        )
        model = models.ChatMessage
