"""Workspace schema mutations."""
import datetime
import uuid

from django.contrib.auth import (
    get_user_model,
)
from django.db import (
    transaction,
)
from django.utils.translation import gettext_lazy as _

import strawberry
from strawberry.arguments import (
    UNSET,
    is_unset,
)

from .. import (
    models,
)
from . import (
    types,
)


# Add inputs
@strawberry.input
class AddWorkspaceBoardInput:
    """Add workspace board input."""

    workspace_uuid: uuid.UUID
    title: str
    description: str


@strawberry.input
class AddWorkspaceBoardSectionInput:
    """Add workspace board section input."""

    workspace_board_uuid: uuid.UUID
    title: str
    description: str


@strawberry.input
class AddTaskInput:
    """Add task mutation input."""

    workspace_board_section_uuid: uuid.UUID
    title: str
    description: str
    deadline: datetime.datetime | None
    assignee: str | None = UNSET
    sub_tasks: list[str] | None = UNSET


@strawberry.input
class AddLabelInput:
    """AddLabelMutation input."""

    workspace_uuid: uuid.UUID
    name: str
    color: int


@strawberry.input
class AddSubTaskInput:
    """Add sub task mutation input."""

    task_uuid: uuid.UUID
    title: str
    description: str


@strawberry.input
class AddChatMessageInput:
    """AddChatMessageMutation input."""

    task_uuid: uuid.UUID
    text: str


@strawberry.input
class ChangeSubTaskDoneInput:
    """ChangeSubTaskDoneMutation input."""

    sub_task_uuid: uuid.UUID
    done: bool


@strawberry.input
class MoveWorkspaceBoardSectionInput:
    """MoveWorkspaceBoardSectionMutation input."""

    workspace_board_section_uuid: uuid.UUID
    order: int


@strawberry.input
class MoveTaskInput:
    """MoveTask mutation input."""

    task_uuid: uuid.UUID
    workspace_board_section_uuid: uuid.UUID
    order: int


@strawberry.input
class AddUserToWorkspaceInput:
    """Input for AddUserToWorkspaceMutation."""

    uuid: uuid.UUID
    email: str


@strawberry.input
class RemoveUserFromWorkspaceInput:
    """Input for RemoveUserFromWorkspaceMutation."""

    uuid: uuid.UUID
    email: str


@strawberry.input
class AssignTaskInput:
    """Input for AssignTaskMutation."""

    uuid: uuid.UUID
    email: str | None


@strawberry.input
class DuplicateTaskInput:
    """DuplicateTaskMutation input."""

    uuid: uuid.UUID


@strawberry.input
class AssignLabelInput:
    """Input for AssignLabelMutation."""

    task_uuid: uuid.UUID
    label_uuid: uuid.UUID
    assigned: bool


@strawberry.input
class UpdateWorkspaceInput:
    """Input for UpdateWorkspaceMutation."""

    uuid: uuid.UUID
    title: str
    description: str


@strawberry.input
class ArchiveWorkspaceBoardInput:
    """Input for ArchiveWorkspaceBoardMutation."""

    uuid: uuid.UUID
    archived: bool


@strawberry.input
class UpdateWorkspaceBoardInput:
    """Input for UpdateWorkspaceBoardMutation."""

    uuid: uuid.UUID
    title: str
    description: str
    deadline: datetime.datetime | None


@strawberry.input
class UpdateWorkspaceBoardSectionInput:
    """Input for UpdateWorkspaceSectionMutation."""

    uuid: uuid.UUID
    title: str
    description: str


@strawberry.input
class UpdateTaskInput:
    """Input for UpdateTaskMutation."""

    uuid: uuid.UUID
    title: str
    description: str
    deadline: datetime.datetime | None


@strawberry.input
class UpdateLabelInput:
    """Input for UpdateLabelMutation."""

    uuid: uuid.UUID
    color: int
    name: str


@strawberry.input
class UpdateSubTaskInput:
    """Input for UpdateSubTaskMutationInput."""

    uuid: uuid.UUID
    title: str
    description: str


@strawberry.input
class DeleteWorkspaceBoardInput:
    """DeleteWorkspaceBoardMutation input."""

    uuid: uuid.UUID


@strawberry.input
class DeleteWorkspaceBoardSectionInput:
    """DeleteWorkspaceBoardSectionMutation input."""

    uuid: uuid.UUID


@strawberry.input
class DeleteTaskInput:
    """DeleteTaskMutation input."""

    uuid: uuid.UUID


@strawberry.input
class DeleteLabelInput:
    """DeleteLabelMutation input."""

    uuid: uuid.UUID


@strawberry.input
class DeleteSubTaskInput:
    """DeleteTaskMutation input."""

    uuid: uuid.UUID


@strawberry.type
class Mutation:
    """Mutation."""

    # Add mutations
    @strawberry.field
    def add_workspace_board(
        self, info, input: AddWorkspaceBoardInput
    ) -> types.WorkspaceBoard:
        """Add workspace board."""
        workspace = models.Workspace.objects.get_for_user_and_uuid(
            info.context.user,
            input.workspace_uuid,
        )
        workspace_board = workspace.add_workspace_board(
            title=input.title,
            description=input.description,
        )
        return workspace_board

    @strawberry.field
    def add_workspace_board_section(
        self, info, input: AddWorkspaceBoardSectionInput
    ) -> types.WorkspaceBoardSection:
        """Add workspace board section."""
        workspace_board = models.WorkspaceBoard.objects.get_for_user_and_uuid(
            info.context.user,
            input.workspace_board_uuid,
        )
        workspace_board_section = workspace_board.add_workspace_board_section(
            title=input.title,
            description=input.description,
        )
        return workspace_board_section

    @strawberry.field
    def add_task(self, info, input: AddTaskInput) -> types.Task:
        """Add task."""
        workspace_board_section = (
            models.WorkspaceBoardSection.objects.get_for_user_and_uuid(
                info.context.user,
                input.workspace_board_section_uuid,
            )
        )
        task = workspace_board_section.add_task(
            input.title,
            input.description,
            input.deadline,
        )
        if not is_unset(input.assignee):
            User = get_user_model()
            user = User.objects.get_by_natural_key(input.assignee)
            task.assign_to(user)
        if not is_unset(input.sub_tasks):
            for title in input.sub_tasks:
                task.add_sub_task(
                    title,
                    "",
                )
        return task

    @strawberry.field
    def add_label(self, info, input: AddLabelInput) -> types.Label:
        """Add label."""
        workspace = models.Workspace.objects.get_for_user_and_uuid(
            info.context.user,
            input.workspace_uuid,
        )
        label = workspace.label_set.create(
            name=input.name,
            color=input.color,
        )
        return label

    @strawberry.field
    def add_sub_task(self, info, input: AddSubTaskInput) -> types.SubTask:
        """Add sub task."""
        task = models.Task.objects.get_for_user_and_uuid(
            info.context.user,
            input.task_uuid,
        )
        sub_task = task.add_sub_task(
            input.title,
            input.description,
        )
        return sub_task

    @strawberry.field
    def add_chat_message(
        self, info, input: AddChatMessageInput
    ) -> types.ChatMessage:
        """Add chat message."""
        task = models.Task.objects.get_for_user_and_uuid(
            info.context.user,
            input.task_uuid,
        )
        chat_message = task.add_chat_message(
            text=input.text,
            author=info.context.user,
        )
        return chat_message

    @strawberry.field
    def change_sub_task_done(
        self, info, input: ChangeSubTaskDoneInput
    ) -> types.SubTask:
        """Change sub task done status."""
        sub_task = models.SubTask.objects.get_for_user_and_uuid(
            info.context.user,
            input.sub_task_uuid,
        )
        sub_task.done = input.done
        sub_task.save()
        return sub_task

    @strawberry.field
    def move_workspace_board_section(
        self, info, input: MoveWorkspaceBoardSectionInput
    ) -> types.WorkspaceBoardSection:
        """Move workspace board section."""
        workspace_board_section = (
            models.WorkspaceBoardSection.objects.get_for_user_and_uuid(
                info.context.user,
                input.workspace_board_section_uuid,
            )
        )
        workspace_board_section.move_to(input.order)
        workspace_board_section.refresh_from_db()
        return workspace_board_section

    @strawberry.field
    def move_task(self, info, input: MoveTaskInput) -> types.Task:
        """Move task."""
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
        # Reorder task
        task.move_to(workspace_board_section, input.order)
        # Return task
        return task

    @strawberry.field
    def add_user_to_workspace(
        self, info, input: AddUserToWorkspaceInput
    ) -> types.Workspace:
        """Add user to workspace."""
        # Find workspace
        workspace = models.Workspace.objects.get_for_user_and_uuid(
            info.context.user,
            input.uuid,
        )
        # Find user
        User = get_user_model()
        try:
            user = User.objects.get_by_natural_key(input.email)
            # Assign user to workspace
            workspace.add_user(user)
        except User.DoesNotExist:
            workspace.invite_user(input.email)
        return workspace

    @strawberry.field
    def remove_user_from_workspace(
        self, info, input: RemoveUserFromWorkspaceInput
    ) -> types.Workspace:
        """Remove user from workspace."""
        workspace = models.Workspace.objects.get_for_user_and_uuid(
            info.context.user,
            input.uuid,
        )
        User = get_user_model()
        try:
            user = User.objects.get_by_natural_key(input.email)
            workspace.remove_user(user)
        except User.DoesNotExist:
            workspace.uninvite_user(input.email)
        return workspace

    @strawberry.field
    def assign_task(self, info, input: AssignTaskInput) -> types.Task:
        """Assign task to user."""
        task = models.Task.objects.get_for_user_and_uuid(
            info.context.user,
            input.uuid,
        )
        if input.email is None:
            task.assign_to(None)
        else:
            User = get_user_model()
            assignee = User.objects.get_by_natural_key(input.email)
            task.assign_to(assignee)
        return task

    @strawberry.field
    def duplicate_task(self, info, input: DuplicateTaskInput) -> types.Task:
        """Duplicate a task."""
        task = models.Task.objects.get_for_user_and_uuid(
            info.context.user,
            input.uuid,
        )
        new_task = models.Task.objects.duplicate_task(task)
        return new_task

    @strawberry.field
    def assign_label(self, info, input: AssignLabelInput) -> types.Task:
        """Assign or unassign a label."""
        task = models.Task.objects.get_for_user_and_uuid(
            info.context.user,
            input.task_uuid,
        )
        label = models.Label.objects.get_for_user_and_uuid(
            info.context.user,
            input.label_uuid,
        )
        if input.assigned:
            task.add_label(label)
        else:
            task.remove_label(label)
        return task

    # Update
    @strawberry.field
    def update_workspace(
        self, info, input: UpdateWorkspaceInput
    ) -> types.Workspace:
        """Update workspace."""
        workspace = models.Workspace.objects.get_for_user_and_uuid(
            info.context.user,
            input.uuid,
        )
        workspace.title = input.title
        workspace.description = input.description
        workspace.save()
        return workspace

    @strawberry.field
    def archive_workspace_board(
        self, info, input: ArchiveWorkspaceBoardInput
    ) -> types.WorkspaceBoard:
        """Archive workspace board."""
        workspace_board = models.WorkspaceBoard.objects.get_for_user_and_uuid(
            info.context.user,
            input.uuid,
        )
        if input.archived:
            workspace_board.archive()
        else:
            workspace_board.unarchive()
        return workspace_board

    @strawberry.field
    def update_workspace_board(
        self, info, input: UpdateWorkspaceBoardInput
    ) -> types.WorkspaceBoard:
        """Update workspace board."""
        workspace_board = models.WorkspaceBoard.objects.get_for_user_and_uuid(
            info.context.user,
            input.uuid,
        )
        workspace_board.title = input.title
        workspace_board.description = input.description
        if input.deadline:
            assert input.deadline.tzinfo
            workspace_board.deadline = input.deadline
        else:
            workspace_board.deadline = None
        workspace_board.save()
        return workspace_board

    @strawberry.field
    def update_workspace_board_section(
        self, info, input: UpdateWorkspaceBoardSectionInput
    ) -> types.WorkspaceBoardSection:
        """Update workspace board."""
        workspace_board_section = (
            models.WorkspaceBoardSection.objects.get_for_user_and_uuid(
                info.context.user,
                input.uuid,
            )
        )
        workspace_board_section.title = input.title
        workspace_board_section.description = input.description
        workspace_board_section.save()
        return workspace_board_section

    @strawberry.field
    def update_task(self, info, input: UpdateTaskInput) -> types.Task:
        """Update workspace board."""
        task = models.Task.objects.get_for_user_and_uuid(
            info.context.user,
            input.uuid,
        )
        task.title = input.title
        task.description = input.description
        if input.deadline:
            task.deadline = input.deadline
            assert task.deadline.tzinfo
        else:
            task.deadline = None
        task.save()
        return task

    @strawberry.field
    def update_label(self, info, input: UpdateLabelInput) -> types.Label:
        """Update label."""
        label = models.Label.objects.get_for_user_and_uuid(
            info.context.user,
            input.uuid,
        )
        label.color = input.color
        label.name = input.name
        label.save()
        return label

    @strawberry.field
    def update_sub_task(
        self, info, input: UpdateSubTaskInput
    ) -> types.SubTask:
        """Update workspace board."""
        sub_task = models.SubTask.objects.get_for_user_and_uuid(
            info.context.user,
            input.uuid,
        )
        sub_task.title = input.title
        sub_task.description = input.description
        sub_task.save()
        return sub_task

    # Delete
    @strawberry.field
    def delete_workspace_board(
        self, info, input: DeleteWorkspaceBoardInput
    ) -> types.WorkspaceBoard:
        """Delete workspace board."""
        workspace_board = models.WorkspaceBoard.objects.get_for_user_and_uuid(
            info.context.user,
            input.uuid,
        )
        workspace_board.delete()
        return workspace_board

    @strawberry.field
    def delete_workspace_board_section(
        self, info, input: DeleteWorkspaceBoardSectionInput
    ) -> types.WorkspaceBoardSection:
        """Delete workspace section board."""
        with transaction.atomic():
            workspace_board_section = (
                models.WorkspaceBoardSection.objects.get_for_user_and_uuid(
                    info.context.user,
                    input.uuid,
                )
            )
            task_len = workspace_board_section.task_set.count()
            if task_len:
                raise ValueError(
                    _("This workspace board section still has tasks"),
                )
            workspace_board_section.delete()
            return workspace_board_section

    @strawberry.field
    def delete_task(self, info, input: DeleteTaskInput) -> types.Task:
        """Delete task."""
        task = models.Task.objects.get_for_user_and_uuid(
            info.context.user,
            input.uuid,
        )
        task.delete()
        return task

    @strawberry.field
    def delete_label(self, info, input: DeleteLabelInput) -> types.Label:
        """Delete label."""
        label = models.Label.objects.get_for_user_and_uuid(
            info.context.user,
            input.uuid,
        )
        label.delete()
        return label

    @strawberry.field
    def delete_sub_task(
        self, info, input: DeleteSubTaskInput
    ) -> types.SubTask:
        """Delete task."""
        sub_task = models.SubTask.objects.get_for_user_and_uuid(
            info.context.user,
            input.uuid,
        )
        sub_task.delete()
        return sub_task
