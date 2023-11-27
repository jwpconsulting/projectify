"""Workspace board services."""
from datetime import datetime
from typing import Optional

from django.utils.timezone import (
    now,
)

from projectify.utils import validate_perm
from user.models import User
from workspace.models import WorkspaceBoard
from workspace.models.workspace import Workspace


# Create
def workspace_board_create(
    *,
    who: User,
    workspace: Workspace,
    title: str,
    description: Optional[str] = None,
    deadline: Optional[datetime] = None,
) -> WorkspaceBoard:
    """Create a workspace board inside a given workspace."""
    validate_perm("workspace.can_create_workspace_board", who, workspace)
    return workspace.workspaceboard_set.create(
        title=title,
        description=description,
        deadline=deadline,
    )


# Read
# Update
def workspace_board_update(
    *,
    who: User,
    workspace_board: WorkspaceBoard,
    title: str,
    description: Optional[str],
    deadline: Optional[datetime],
) -> WorkspaceBoard:
    """Update a workspace board."""
    validate_perm("workspace.can_update_workspace_board", who, workspace_board)
    workspace_board.title = title
    workspace_board.description = description
    if deadline and deadline.tzinfo is None:
        raise ValueError(f"tzinfo must be specified, got {deadline}")
    workspace_board.deadline = deadline
    workspace_board.save()
    return workspace_board


# Delete
# RPC
def workspace_board_archive(
    *,
    who: User,
    workspace_board: WorkspaceBoard,
    archived: bool,
) -> WorkspaceBoard:
    """Archive a workspace board, or not."""
    validate_perm(
        "workspace.can_update_workspace_board",
        who,
        workspace_board,
    )
    if archived:
        workspace_board.archived = now()
    else:
        workspace_board.archived = None
    workspace_board.save()
    return workspace_board
