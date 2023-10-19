"""Workspace schema mutations."""
import datetime
import uuid

from django.db import (
    transaction,
)
from django.shortcuts import (
    get_object_or_404,
)
from django.utils.translation import gettext_lazy as _

import strawberry
from strawberry.unset import (
    UNSET,
)

from graphql import (
    GraphQLResolveInfo,
)
from projectify.utils import (
    get_user_model,
)
from workspace.models.workspace_user_invite import (
    add_or_invite_workspace_user,
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
    deadline: datetime.datetime | None = UNSET


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
    labels: list[uuid.UUID] | None = UNSET


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


# Update inputs
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
class MoveTaskAfterInput:
    """MoveTaskAfter mutation input."""

    task_uuid: uuid.UUID
    workspace_board_section_uuid: uuid.UUID
    after_task_uuid: uuid.UUID | None = UNSET


@strawberry.input
class MoveSubTaskInput:
    """MoveSubTask mutation input."""

    sub_task_uuid: uuid.UUID
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
class UpdateWorkspaceUserInput:
    """Input for UpdateWorkspaceUserMutation."""

    email: str
    workspace_uuid: uuid.UUID
    role: types.WorkspaceUserRole
    job_title: str


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


# Delete inputs
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
        self, info: GraphQLResolveInfo, input: AddWorkspaceBoardInput
    ) -> types.WorkspaceBoard:
        """Add workspace board."""
        qs = models.Workspace.objects.filter_for_user_and_uuid(
            info.context.user,
            input.workspace_uuid,
        )
        workspace = get_object_or_404(qs)
        assert info.context.user.has_perm(
            "workspace.can_create_workspace_board", workspace
        )
        if input.deadline is not UNSET and input.deadline:
            assert input.deadline.tzinfo
            deadline = input.deadline
        else:
            deadline = None
        workspace_board = workspace.add_workspace_board(
            title=input.title,
            description=input.description,
            deadline=deadline,
        )
        return workspace_board

    @strawberry.field
    def add_workspace_board_section(
        self, info: GraphQLResolveInfo, input: AddWorkspaceBoardSectionInput
    ) -> types.WorkspaceBoardSection:
        """Add workspace board section."""
        qs = models.WorkspaceBoard.objects.filter_for_user_and_uuid(
            info.context.user,
            input.workspace_board_uuid,
        )
        workspace_board = get_object_or_404(qs)
        assert info.context.user.has_perm(
            "workspace.can_create_workspace_board_section", workspace_board
        )
        workspace_board_section = workspace_board.add_workspace_board_section(
            title=input.title,
            description=input.description,
        )
        return workspace_board_section

    @strawberry.field
    def add_task(
        self, info: GraphQLResolveInfo, input: AddTaskInput
    ) -> types.Task:
        """Add task."""
        qs = models.WorkspaceBoardSection.objects.filter_for_user_and_uuid(
            info.context.user,
            input.workspace_board_section_uuid,
        )
        workspace_board_section = get_object_or_404(qs)
        assert info.context.user.has_perm(
            "workspace.can_create_task", workspace_board_section
        )
        task = workspace_board_section.add_task(
            input.title,
            input.description,
            input.deadline,
        )
        if input.assignee is not UNSET:
            User = get_user_model()
            user = User.objects.get_by_natural_key(input.assignee)
            workspace_user = (
                workspace_board_section.workspace.workspaceuser_set.get(
                    user=user
                )
            )
            task.assign_to(workspace_user)
        if input.sub_tasks is not UNSET and input.sub_tasks is not None:
            for title in input.sub_tasks:
                task.add_sub_task(
                    title,
                    "",
                )
        if input.labels is not UNSET and input.labels is not None:
            for label_uuid in input.labels:
                label_qs = models.Label.objects.filter_for_user_and_uuid(
                    info.context.user,
                    label_uuid,
                )
                label = get_object_or_404(label_qs)
                task.add_label(label)
        return task  # type: ignore

    @strawberry.field
    def add_label(
        self, info: GraphQLResolveInfo, input: AddLabelInput
    ) -> types.Label:
        """Add label."""
        qs = models.Workspace.objects.filter_for_user_and_uuid(
            info.context.user,
            input.workspace_uuid,
        )
        workspace = get_object_or_404(qs)
        assert info.context.user.has_perm(
            "workspace.can_create_label", workspace
        )
        label = workspace.label_set.create(
            name=input.name,
            color=input.color,
        )
        return label

    @strawberry.field
    def add_sub_task(
        self, info: GraphQLResolveInfo, input: AddSubTaskInput
    ) -> types.SubTask:
        """Add sub task."""
        qs = models.Task.objects.filter_for_user_and_uuid(
            info.context.user,
            input.task_uuid,
        )
        task = get_object_or_404(qs)
        assert info.context.user.has_perm(
            "workspace.can_create_sub_task", task
        )
        sub_task = task.add_sub_task(
            input.title,
            input.description,
        )
        return sub_task

    @strawberry.field
    def add_chat_message(
        self, info: GraphQLResolveInfo, input: AddChatMessageInput
    ) -> types.ChatMessage:
        """Add chat message."""
        qs = models.Task.objects.filter_for_user_and_uuid(
            info.context.user,
            input.task_uuid,
        )
        task = get_object_or_404(qs)
        assert info.context.user.has_perm(
            "workspace.can_create_chat_message", task
        )
        chat_message = task.add_chat_message(
            text=input.text,
            author=info.context.user,
        )
        return chat_message

    @strawberry.field
    def change_sub_task_done(
        self, info: GraphQLResolveInfo, input: ChangeSubTaskDoneInput
    ) -> types.SubTask:
        """Change sub task done status."""
        qs = models.SubTask.objects.filter_for_user_and_uuid(
            info.context.user,
            input.sub_task_uuid,
        )
        sub_task = get_object_or_404(qs)
        assert info.context.user.has_perm(
            "workspace.can_update_sub_task", sub_task
        )
        sub_task.done = input.done
        sub_task.save()
        return sub_task

    @strawberry.field
    def move_workspace_board_section(
        self, info: GraphQLResolveInfo, input: MoveWorkspaceBoardSectionInput
    ) -> types.WorkspaceBoardSection:
        """Move workspace board section."""
        qs = models.WorkspaceBoardSection.objects.filter_for_user_and_uuid(
            info.context.user,
            input.workspace_board_section_uuid,
        )
        workspace_board_section = get_object_or_404(qs)
        assert info.context.user.has_perm(
            "workspace.can_update_workspace_board_section",
            workspace_board_section,
        )
        workspace_board_section.move_to(input.order)
        workspace_board_section.refresh_from_db()
        return workspace_board_section

    @strawberry.field
    def move_task(
        self, info: GraphQLResolveInfo, input: MoveTaskInput
    ) -> types.Task:
        """Move task."""
        # Find workspace board section
        qs: models.WorkspaceBoardSectionQuerySet = (
            models.WorkspaceBoardSection.objects.filter_for_user_and_uuid(
                info.context.user,
                input.workspace_board_section_uuid,
            )
        )
        workspace_board_section = get_object_or_404(qs)
        # Find task
        task_qs: models.TaskQuerySet = (
            models.Task.objects.filter_for_user_and_uuid(
                info.context.user,
                input.task_uuid,
            )
        )
        task: models.Task = get_object_or_404(task_qs)
        assert info.context.user.has_perm("workspace.can_update_task", task)
        # Reorder task
        task.move_to(workspace_board_section, input.order)
        # Return task
        task.refresh_from_db()
        return task  # type: ignore

    @strawberry.field
    def move_task_after(
        self, info: GraphQLResolveInfo, input: MoveTaskAfterInput
    ) -> types.Task:
        """Move task after another task."""
        # Find workspace board section
        workspace_board_section_qs = (
            models.WorkspaceBoardSection.objects.filter_for_user_and_uuid(
                info.context.user,
                input.workspace_board_section_uuid,
            )
        )
        workspace_board_section = get_object_or_404(workspace_board_section_qs)
        # Find task
        task_qs = models.Task.objects.filter_for_user_and_uuid(
            info.context.user,
            input.task_uuid,
        )
        task = get_object_or_404(task_qs)
        assert info.context.user.has_perm("workspace.can_update_task", task)
        # Find after task
        if input.after_task_uuid is not UNSET and input.after_task_uuid:
            after_task = models.Task.objects.filter_for_user_and_uuid(
                info.context.user,
                input.after_task_uuid,
            ).get()
            new_order = after_task._order
        else:
            new_order = 0
        # Reorder task
        task.move_to(workspace_board_section, new_order)
        # Return task
        task.refresh_from_db()
        return task

    @strawberry.field
    def move_sub_task(
        self, info: GraphQLResolveInfo, input: MoveSubTaskInput
    ) -> types.SubTask:
        """Move sub task to a specified position."""
        # Find sub task
        qs = models.SubTask.objects.filter_for_user_and_uuid(
            info.context.user,
            input.sub_task_uuid,
        )
        sub_task = get_object_or_404(qs)
        assert info.context.user.has_perm(
            "workspace.can_update_sub_task", sub_task
        )
        # Reorder sub task
        sub_task.move_to(input.order)
        # This is necessary to refresh the _order field
        sub_task.refresh_from_db()
        return sub_task

    @strawberry.field
    def add_user_to_workspace(
        self, info: GraphQLResolveInfo, input: AddUserToWorkspaceInput
    ) -> types.Workspace:
        """Add user to workspace."""
        # Find workspace
        qs = models.Workspace.objects.filter_for_user_and_uuid(
            info.context.user,
            input.uuid,
        )
        workspace = get_object_or_404(qs)
        assert info.context.user.has_perm(
            "workspace.can_create_workspace_user", workspace
        )
        add_or_invite_workspace_user(workspace, input.email)
        return workspace

    @strawberry.field
    def remove_user_from_workspace(
        self, info: GraphQLResolveInfo, input: RemoveUserFromWorkspaceInput
    ) -> types.Workspace:
        """Remove user from workspace."""
        qs = models.Workspace.objects.filter_for_user_and_uuid(
            info.context.user,
            input.uuid,
        )
        workspace = get_object_or_404(qs)
        assert info.context.user.has_perm(
            "workspace.can_delete_workspace_user", workspace
        )
        User = get_user_model()
        try:
            user = User.objects.get_by_natural_key(input.email)
            workspace.remove_user(user)
        except User.DoesNotExist:
            workspace.uninvite_user(input.email)
        return workspace

    @strawberry.field
    def assign_task(
        self, info: GraphQLResolveInfo, input: AssignTaskInput
    ) -> types.Task:
        """Assign task to user."""
        qs = models.Task.objects.filter_for_user_and_uuid(
            info.context.user,
            input.uuid,
        )
        task = get_object_or_404(qs)
        assert info.context.user.has_perm("workspace.can_update_task", task)
        if input.email is None:
            task.assign_to(None)
        else:
            User = get_user_model()
            assignee = User.objects.get_by_natural_key(input.email)
            workspace_user = task.workspace.workspaceuser_set.get(
                user=assignee
            )
            task.assign_to(workspace_user)
        return task

    @strawberry.field
    def duplicate_task(
        self, info: GraphQLResolveInfo, input: DuplicateTaskInput
    ) -> types.Task:
        """Duplicate a task."""
        qs = models.Task.objects.filter_for_user_and_uuid(
            info.context.user,
            input.uuid,
        )
        task = get_object_or_404(qs)
        assert info.context.user.has_perm(
            "workspace.can_create_task",
            task.workspace,
        )
        new_task = models.Task.objects.duplicate_task(task)
        return new_task

    @strawberry.field
    def assign_label(
        self, info: GraphQLResolveInfo, input: AssignLabelInput
    ) -> types.Task:
        """Assign or unassign a label."""
        task_qs = models.Task.objects.filter_for_user_and_uuid(
            info.context.user,
            input.task_uuid,
        )
        task = get_object_or_404(task_qs)
        label_qs = models.Label.objects.filter_for_user_and_uuid(
            info.context.user,
            input.label_uuid,
        )
        label = get_object_or_404(label_qs)
        if input.assigned:
            assert info.context.user.has_perm(
                "workspace.can_create_task_label",
                task,
            )
            task.add_label(label)
        else:
            assert info.context.user.has_perm(
                "workspace.can_delete_task_label",
                task,
            )
            task.remove_label(label)
        return task

    # Update
    @strawberry.field
    def update_workspace(
        self, info: GraphQLResolveInfo, input: UpdateWorkspaceInput
    ) -> types.Workspace:
        """Update workspace."""
        qs = models.Workspace.objects.filter_for_user_and_uuid(
            info.context.user,
            input.uuid,
        )
        workspace = get_object_or_404(qs)
        assert info.context.user.has_perm(
            "workspace.can_update_workspace",
            workspace,
        )
        workspace.title = input.title
        workspace.description = input.description
        workspace.save()
        return workspace

    @strawberry.field
    def update_workspace_user(
        self, info: GraphQLResolveInfo, input: UpdateWorkspaceUserInput
    ) -> types.WorkspaceUser:
        """Update workspace user."""
        qs = models.Workspace.objects.filter_for_user_and_uuid(
            info.context.user,
            input.workspace_uuid,
        )
        workspace = get_object_or_404(qs)
        User = get_user_model()
        user = User.objects.get_by_natural_key(input.email)
        workspace_user = (
            models.WorkspaceUser.objects.get_by_workspace_and_user(
                workspace,
                user,
            )
        )
        assert info.context.user.has_perm(
            "workspace.can_update_workspace_user", workspace_user
        )
        t = types.WorkspaceUserRole
        workspace_user.role = {
            t.OBSERVER: models.WorkspaceUserRoles.OBSERVER,
            t.MEMBER: models.WorkspaceUserRoles.MEMBER,
            t.MAINTAINER: models.WorkspaceUserRoles.MAINTAINER,
            t.OWNER: models.WorkspaceUserRoles.OWNER,
        }[input.role]
        workspace_user.job_title = input.job_title
        workspace_user.save()
        return workspace_user

    @strawberry.field
    def archive_workspace_board(
        self, info: GraphQLResolveInfo, input: ArchiveWorkspaceBoardInput
    ) -> types.WorkspaceBoard:
        """Archive workspace board."""
        qs = models.WorkspaceBoard.objects.filter_for_user_and_uuid(
            info.context.user,
            input.uuid,
        )
        workspace_board = get_object_or_404(qs)
        assert info.context.user.has_perm(
            "workspace.can_update_workspace_board",
            workspace_board,
        )
        if input.archived:
            workspace_board.archive()
        else:
            workspace_board.unarchive()
        return workspace_board

    @strawberry.field
    def update_workspace_board(
        self, info: GraphQLResolveInfo, input: UpdateWorkspaceBoardInput
    ) -> types.WorkspaceBoard:
        """Update workspace board."""
        qs = models.WorkspaceBoard.objects.filter_for_user_and_uuid(
            info.context.user,
            input.uuid,
        )
        workspace_board = get_object_or_404(qs)
        assert info.context.user.has_perm(
            "workspace.can_update_workspace_board",
            workspace_board,
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
        self, info: GraphQLResolveInfo, input: UpdateWorkspaceBoardSectionInput
    ) -> types.WorkspaceBoardSection:
        """Update workspace board."""
        qs = models.WorkspaceBoardSection.objects.filter_for_user_and_uuid(
            info.context.user,
            input.uuid,
        )
        workspace_board_section = get_object_or_404(qs)
        assert info.context.user.has_perm(
            "workspace.can_update_workspace_board_section",
            workspace_board_section,
        )
        workspace_board_section.title = input.title
        workspace_board_section.description = input.description
        workspace_board_section.save()
        return workspace_board_section

    @strawberry.field
    def update_task(
        self, info: GraphQLResolveInfo, input: UpdateTaskInput
    ) -> types.Task:
        """Update workspace board."""
        qs = models.Task.objects.filter_for_user_and_uuid(
            info.context.user,
            input.uuid,
        )
        task = get_object_or_404(qs)
        assert info.context.user.has_perm(
            "workspace.can_update_task",
            task,
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
    def update_label(
        self, info: GraphQLResolveInfo, input: UpdateLabelInput
    ) -> types.Label:
        """Update label."""
        qs = models.Label.objects.filter_for_user_and_uuid(
            info.context.user,
            input.uuid,
        )
        label = get_object_or_404(qs)
        assert info.context.user.has_perm(
            "workspace.can_update_label",
            label,
        )
        label.color = input.color
        label.name = input.name
        label.save()
        return label

    @strawberry.field
    def update_sub_task(
        self, info: GraphQLResolveInfo, input: UpdateSubTaskInput
    ) -> types.SubTask:
        """Update workspace board."""
        qs = models.SubTask.objects.filter_for_user_and_uuid(
            info.context.user,
            input.uuid,
        )
        sub_task = get_object_or_404(qs)
        assert info.context.user.has_perm(
            "workspace.can_update_sub_task",
            sub_task,
        )
        sub_task.title = input.title
        sub_task.description = input.description
        sub_task.save()
        return sub_task

    # Delete
    @strawberry.field
    def delete_workspace_board(
        self, info: GraphQLResolveInfo, input: DeleteWorkspaceBoardInput
    ) -> types.WorkspaceBoard:
        """Delete workspace board."""
        qs = models.WorkspaceBoard.objects.filter_for_user_and_uuid(
            info.context.user,
            input.uuid,
        )
        workspace_board = get_object_or_404(qs)
        assert info.context.user.has_perm(
            "workspace.can_delete_workspace_board",
            workspace_board,
        )
        workspace_board.delete()
        return workspace_board

    @strawberry.field
    def delete_workspace_board_section(
        self, info: GraphQLResolveInfo, input: DeleteWorkspaceBoardSectionInput
    ) -> types.WorkspaceBoardSection:
        """Delete workspace section board."""
        with transaction.atomic():
            qs = models.WorkspaceBoardSection.objects.filter_for_user_and_uuid(
                info.context.user,
                input.uuid,
            )
            workspace_board_section = get_object_or_404(qs)
            assert info.context.user.has_perm(
                "workspace.can_delete_workspace_board_section",
                workspace_board_section,
            )
            task_len = workspace_board_section.task_set.count()
            if task_len:
                raise ValueError(
                    _("This workspace board section still has tasks"),
                )
            workspace_board_section.delete()
            return workspace_board_section

    @strawberry.field
    def delete_task(
        self, info: GraphQLResolveInfo, input: DeleteTaskInput
    ) -> types.Task:
        """Delete task."""
        qs = models.Task.objects.filter_for_user_and_uuid(
            info.context.user,
            input.uuid,
        )
        task = get_object_or_404(qs)
        assert info.context.user.has_perm(
            "workspace.can_delete_task",
            task,
        )
        task.delete()
        return task

    @strawberry.field
    def delete_label(
        self, info: GraphQLResolveInfo, input: DeleteLabelInput
    ) -> types.Label:
        """Delete label."""
        qs = models.Label.objects.filter_for_user_and_uuid(
            info.context.user,
            input.uuid,
        )
        label = get_object_or_404(qs)
        assert info.context.user.has_perm(
            "workspace.can_delete_label",
            label,
        )
        label.delete()
        return label

    @strawberry.field
    def delete_sub_task(
        self, info: GraphQLResolveInfo, input: DeleteSubTaskInput
    ) -> types.SubTask:
        """Delete task."""
        qs = models.SubTask.objects.filter_for_user_and_uuid(
            info.context.user,
            input.uuid,
        )
        sub_task = get_object_or_404(qs)
        assert info.context.user.has_perm(
            "workspace.can_delete_sub_task",
            sub_task,
        )
        sub_task.delete()
        return sub_task
