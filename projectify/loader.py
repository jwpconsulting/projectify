"""Loader module."""
from workspace.schema import loader as workspace_loader


class Loader:
    """Combine all loaders into one."""

    def __init__(self):
        """Initialize the loaders."""
        self.workspace_user_loader = workspace_loader.WorkspaceUserLoader()
        self.workspace_workspace_board_loader = (
            workspace_loader.WorkspaceWorkspaceBoardLoader()
        )
        self.workspace_archived_workspace_board_loader = (
            workspace_loader.WorkspaceArchivedWorkspaceBoardLoader()
        )
        self.workspace_label_loader = workspace_loader.WorkspaceLabelLoader()
        self.workspace_board_workspace_board_section_loader = (
            workspace_loader.WorkspaceBoardWorkspaceBoardSectionLoader()
        )
        self.workspace_board_section_task_loader = (
            workspace_loader.WorkspaceBoardSectionTaskLoader()
        )
        self.task_sub_task_loader = workspace_loader.TaskSubTaskLoader()
        self.task_chat_message_loader = (
            workspace_loader.TaskChatMessageLoader()
        )
        self.task_task_label_loader = workspace_loader.TaskTaskLabelLoader()
        self.user_loader = workspace_loader.UserLoader()
        self.workspace_loader = workspace_loader.WorkspaceLoader()
        self.workspace_board_loader = workspace_loader.WorkspaceBoardLoader()
        self.workspace_board_section_loader = (
            workspace_loader.WorkspaceBoardSectionLoader()
        )
        self.task_loader = workspace_loader.TaskLoader()
