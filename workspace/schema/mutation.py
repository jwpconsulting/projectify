"""Workspace schema mutations."""
import graphene

from .. import (
    models,
)
from . import (
    types,
)


class AddWorkspaceBoardInput(graphene.InputObjectType):
    """Add workspace board input."""

    workspace_uuid = graphene.ID(required=True)
    title = graphene.String(required=True)
    description = graphene.String(required=True)


class AddWorkspaceBoardMutation(graphene.Mutation):
    """Add workspace board mutation."""

    class Arguments:
        """Arguments."""

        input = AddWorkspaceBoardInput(required=True)

    workspace_board = graphene.Field(types.WorkspaceBoard)

    @classmethod
    def mutate(cls, root, info, input):
        """Mutate."""
        workspace = models.Workspace.objects.get_for_user_and_uuid(
            info.context.user,
            input.workspace_uuid,
        )
        workspace_board = workspace.add_workspace_board(
            title=input.title,
            description=input.description,
        )
        return cls(workspace_board)


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

    workspace_board_section = graphene.Field(types.WorkspaceBoardSection)

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

    task = graphene.Field(types.Task)

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


class AddSubTaskInput(graphene.InputObjectType):
    """Add sub task mutation input."""

    task_uuid = graphene.ID(required=True)
    title = graphene.String(required=True)
    description = graphene.String(required=True)


class AddSubTaskMutation(graphene.Mutation):
    """Add subtask mutation."""

    class Arguments:
        """Arguments."""

        input = AddSubTaskInput(required=True)

    sub_task = graphene.Field(types.SubTask)

    @classmethod
    def mutate(cls, root, info, input):
        """Mutate."""
        task = models.Task.objects.get_for_user_and_uuid(
            info.context.user,
            input.task_uuid,
        )
        sub_task = task.add_task(
            input.title,
            input.description,
        )
        return cls(sub_task)


class MoveTaskInput(graphene.InputObjectType):
    """MoveTask mutation input."""

    task_uuid = graphene.ID(required=True)
    workspace_board_section_uuid = graphene.ID(required=True)
    position = graphene.Int(required=True)


class MoveTaskMutation(graphene.Mutation):
    """Move task mutation."""

    class Arguments:
        """Arguments."""

        input = MoveTaskInput(required=True)

    task = graphene.Field(types.Task)

    @classmethod
    def mutate(cls, root, info, input):
        """Mutate."""
        # Find workspace board section
        workspace_board_section = (
            models.WorkspaceBoardSection.objects.get_for_user_and_uuid(
                info.context.user,
                input.workspace_board_section_uuid,
            )
        )
        # Find task
        task = models.Task.objects.get_for_user_and_uuid(
            info.context.user,
            input.task_uuid,
        )
        # Reposition task
        task.move_to(workspace_board_section, input.position)
        # Return task
        return cls(task)


class Mutation:
    """Mutation."""

    add_workspace_board = AddWorkspaceBoardMutation.Field()
    add_workspace_board_section = AddWorkspaceBoardSectionMutation.Field()
    add_task = AddTaskMutation.Field()
    add_sub_task = AddSubTaskMutation.Field()
    move_task = MoveTaskMutation.Field()
