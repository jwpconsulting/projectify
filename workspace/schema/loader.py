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
