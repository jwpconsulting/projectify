"""Workspace board services."""
from datetime import datetime
from typing import Optional

from workspace.models import WorkspaceBoard
from workspace.models.workspace import Workspace


def workspace_board_create(
    *,
    workspace: Workspace,
    title: str,
    description: Optional[str] = None,
    deadline: Optional[datetime] = None,
) -> WorkspaceBoard:
    """Create a workspace board inside a given workspace."""
    return workspace.workspaceboard_set.create(
        title=title,
        description=description,
        deadline=deadline,
    )
