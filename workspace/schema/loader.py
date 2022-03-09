"""Workspace schema loader."""
from collections import (
    defaultdict,
)

from django.contrib.auth import (
    get_user_model,
)

from promise import (
    Promise,
)
from promise.dataloader import (
    DataLoader,
)

from .. import (
    models,
)
from . import (
    types,
)


class WorkspaceUserLoader(DataLoader):
    """Workspace user loader."""

    def batch_load_fn(self, keys):
        """
        Load users for workspaces.

        Input is [workspace1.pk, workspace2.pk, ...]
        """
        users = defaultdict(list)
        qs = models.WorkspaceUser.objects.filter_by_workspace_pks(
            keys,
        ).select_related(
            "workspace",
            "user",
        )
        for workspace_user in qs.iterator():
            users[workspace_user.workspace.pk].append(workspace_user.user)
        return Promise.resolve([users.get(key, []) for key in keys])


class WorkspaceWorkspaceBoardLoader(DataLoader):
    """Workspace board loader for workspaces."""

    def batch_load_fn(self, keys):
        """Load workspace boards for workspace."""
        workspace_boards = defaultdict(list)
        qs = (
            models.WorkspaceBoard.objects.filter_by_archived(
                False,
            )
            .filter_by_workspace_pks(
                keys,
            )
            .select_related(
                "workspace",
            )
        )
        for workspace_board in qs.iterator():
            workspace_boards[workspace_board.workspace.pk].append(
                workspace_board,
            )
        return Promise.resolve([workspace_boards.get(key, []) for key in keys])


class WorkspaceArchivedWorkspaceBoardLoader(DataLoader):
    """Workspace board loader for archived workspaces."""

    def batch_load_fn(self, keys):
        """Load workspace boards for workspace."""
        workspace_boards = defaultdict(list)
        qs = (
            models.WorkspaceBoard.objects.filter_by_archived(
                True,
            )
            .filter_by_workspace_pks(
                keys,
            )
            .select_related(
                "workspace",
            )
        )
        for workspace_board in qs.iterator():
            workspace_boards[workspace_board.workspace.pk].append(
                workspace_board,
            )
        return Promise.resolve([workspace_boards.get(key, []) for key in keys])


class WorkspaceLabelLoader(DataLoader):
    """Label loader for workspaces."""

    def batch_load_fn(self, keys):
        """Load labels for workspace."""
        labels = defaultdict(list)
        qs = models.Label.objects.filter_by_workspace_pks(
            keys,
        ).select_related(
            "workspace",
        )
        for label in qs.iterator():
            labels[label.workspace.pk].append(label)
        return Promise.resolve([labels.get(key, []) for key in keys])


class WorkspaceUserInviteLoader(DataLoader):
    """User invite loader for workspaces."""

    def batch_load_fn(self, keys):
        """Load user invite for workspace keys."""
        user_invitations = defaultdict(list)
        qs = models.WorkspaceUserInvite.objects.filter_by_workspace_pks(
            keys,
        ).select_related(
            "workspace",
            "user_invite",
        )
        for user_invite in qs.iterator():
            obj = types.UserInvitation(email=user_invite.user_invite.email)
            user_invitations[user_invite.workspace.pk].append(obj)
        return Promise.resolve([user_invitations.get(key, []) for key in keys])


class WorkspaceBoardWorkspaceBoardSectionLoader(DataLoader):
    """Workspace board section loader for workspace boards."""

    def batch_load_fn(self, keys):
        """Load workspace board sections for workspace boards."""
        workspace_board_sections = defaultdict(list)
        objects = models.WorkspaceBoardSection.objects
        qs = objects.filter_by_workspace_board_pks(keys).select_related(
            "workspace_board",
        )
        for workspace_board_section in qs.iterator():
            workspace_board_sections[
                workspace_board_section.workspace_board.pk
            ].append(
                workspace_board_section,
            )
        return Promise.resolve(
            [workspace_board_sections.get(key, []) for key in keys],
        )


class WorkspaceBoardSectionTaskLoader(DataLoader):
    """Task loader for workspace board sections."""

    def batch_load_fn(self, keys):
        """Load tasks for workspace board section keys."""
        tasks = defaultdict(list)
        qs = models.Task.objects.filter_by_workspace_board_section_pks(
            keys,
        ).select_related(
            "workspace_board_section",
        )
        for task in qs.iterator():
            tasks[task.workspace_board_section.pk].append(task)
        return Promise.resolve([tasks.get(key, []) for key in keys])


class TaskSubTaskLoader(DataLoader):
    """SubTask loader for tasks."""

    def batch_load_fn(self, keys):
        """Load sub tasks for task keys."""
        sub_tasks = defaultdict(list)
        qs = models.SubTask.objects.filter_by_task_pks(keys).select_related(
            "task",
        )
        for sub_task in qs.iterator():
            sub_tasks[sub_task.task.pk].append(sub_task)
        return Promise.resolve([sub_tasks.get(key, []) for key in keys])


class TaskChatMessageLoader(DataLoader):
    """ChatMessage loader for tasks."""

    def batch_load_fn(self, keys):
        """Load chat messages for task keys."""
        chat_messages = defaultdict(list)
        qs = models.ChatMessage.objects.filter_by_task_pks(
            keys,
        ).select_related(
            "task",
        )
        for chat_message in qs.iterator():
            chat_messages[chat_message.task.pk].append(chat_message)
        return Promise.resolve([chat_messages.get(key, []) for key in keys])


class TaskTaskLabelLoader(DataLoader):
    """Label loader for tasks."""

    def batch_load_fn(self, keys):
        """
        Load labels for task keys.

        Skip over m2m connection and return labels directly.
        """
        labels = defaultdict(list)
        qs = models.TaskLabel.objects.filter_by_task_pks(
            keys,
        )
        for task_label in qs.iterator():
            labels[task_label.task.pk].append(task_label.label)
        return Promise.resolve([labels.get(key, []) for key in keys])


class UserLoader(DataLoader):
    """Author loader."""

    def batch_load_fn(self, keys):
        """Load authors for author pks."""
        users = {}
        qs = get_user_model().objects.filter(pk__in=keys)
        for user in qs.iterator():
            users[user.pk] = user
        return Promise.resolve([users.get(key) for key in keys])


class WorkspaceLoader(DataLoader):
    """Workspace loader."""

    def batch_load_fn(self, keys):
        """Load work spaces by pk."""
        workspaces = {}
        qs = models.Workspace.objects.filter(pk__in=keys)
        for workspace in qs.iterator():
            workspaces[workspace.pk] = workspace
        return Promise.resolve([workspaces.get(key) for key in keys])


class WorkspaceBoardLoader(DataLoader):
    """Workspace board loader."""

    def batch_load_fn(self, keys):
        """Load work space boards by pk."""
        workspace_boards = {}
        qs = models.WorkspaceBoard.objects.filter(pk__in=keys)
        for workspace_board in qs.iterator():
            workspace_boards[workspace_board.pk] = workspace_board
        return Promise.resolve([workspace_boards.get(key) for key in keys])


class WorkspaceBoardSectionLoader(DataLoader):
    """Workspace board section loader."""

    def batch_load_fn(self, keys):
        """Load tasks by pk."""
        workspace_board_sections = {}
        qs = models.WorkspaceBoardSection.objects.filter(pk__in=keys)
        for workspace_board_section in qs.iterator():
            workspace_board_sections[
                workspace_board_section.pk
            ] = workspace_board_section
        return Promise.resolve(
            [workspace_board_sections.get(key) for key in keys],
        )


class TaskLoader(DataLoader):
    """Task loader."""

    def batch_load_fn(self, keys):
        """Load tasks by pk."""
        tasks = {}
        qs = models.Task.objects.filter(pk__in=keys)
        for task in qs.iterator():
            tasks[task.pk] = task
        return Promise.resolve([tasks.get(key) for key in keys])
