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
    workspace = graphene.Field(Workspace, uuid=graphene.ID())
    workspace_board = graphene.Field(WorkspaceBoard, uuid=graphene.ID())
    workspace_board_section = graphene.Field(
        WorkspaceBoardSection,
        uuid=graphene.ID(),
    )
    task = graphene.Field(Task, uuid=graphene.ID())

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


class AddWorkspaceBoardSectionInput(graphene.InputObjectType):
    """Add workspace board section input."""

    workspace_board_uuid = graphene.ID(required=True)
    title = graphene.ID(required=True)
    description = graphene.ID(required=True)


class AddWorkspaceBoardSectionMutation(graphene.Mutation):
    """Add workspace board section mutation."""

    class Arguments:
        """Arguments."""

        input = AddWorkspaceBoardSectionInput(required=True)

    workspace_board_section = graphene.Field(WorkspaceBoardSection)

    @classmethod
    def mutate(cls, root, info, input):
        """Mutate."""
        workspace_board = models.WorkspaceBoard.objects.get_for_user_and_uuid(
            info.context.user,
            input.workspace_board_uuid,
        )
        workspace_board_section = workspace_board.add_workspace_board_section(
            title=input.title,
            description=input.description,
        )
        return cls(workspace_board_section)


class AddTaskMutationInput(graphene.InputObjectType):
    """Add task mutation input."""

    workspace_board_section_uuid = graphene.ID(required=True)
    title = graphene.String(required=True)
    description = graphene.String(required=True)


class AddTaskMutation(graphene.Mutation):
    """Add task mutation."""

    class Arguments:
        """Arguments."""

        input = AddTaskMutationInput(required=True)

    task = graphene.Field(Task)

    @classmethod
    def mutate(cls, root, info, input):
        """Mutate."""
        workspace_board_section = (
            models.WorkspaceBoardSection.objects.get_for_user_and_uuid(
                info.context.user,
                input.workspace_board_section_uuid,
            )
        )
        task = workspace_board_section.add_task(
            input.title,
            input.description,
        )
        return cls(task)


class Mutation:
    """Mutation."""

    add_workspace_board_section = AddWorkspaceBoardSectionMutation.Field()
    add_task = AddTaskMutation.Field()
