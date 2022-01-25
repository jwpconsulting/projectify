"""Workspace schema loader."""
from collections import (
    defaultdict,
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


workspace_user_loader = WorkspaceUserLoader()


class WorkspaceWorkspaceBoardLoader(DataLoader):
    """Workspace board loader for workspaces."""

    def batch_load_fn(self, keys):
        """Load workspace boards for workspace."""
        workspace_boards = defaultdict(list)
        qs = models.WorkspaceBoard.objects.filter_by_workspace_pks(
            keys,
        ).select_related(
            "workspace",
        )
        for workspace_board in qs.iterator():
            workspace_boards[workspace_board.workspace.pk].append(
                workspace_board,
            )
        return Promise.resolve([workspace_boards.get(key, []) for key in keys])


workspace_workspace_board_loader = WorkspaceWorkspaceBoardLoader()


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


workspace_board_workspace_board_section_loader = (
    WorkspaceBoardWorkspaceBoardSectionLoader()
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


workspace_board_section_task_loader = WorkspaceBoardSectionTaskLoader()


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


task_sub_task_loader = TaskSubTaskLoader()
