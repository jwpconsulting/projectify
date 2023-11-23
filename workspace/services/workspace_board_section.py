"""Workspace board section services."""

from typing import Optional

from projectify.utils import validate_perm
from user.models import User
from workspace.models import WorkspaceBoard, WorkspaceBoardSection


def workspace_board_section_create(
    *,
    who: User,
    title: str,
    description: Optional[str] = None,
    workspace_board: WorkspaceBoard,
) -> WorkspaceBoardSection:
    """Create a workspace board section."""
    validate_perm(
        "workspace.can_create_workspace_board_section",
        who,
        workspace_board,
    )
    workspace_board_section = WorkspaceBoardSection(
        title=title,
        description=description,
        workspace_board=workspace_board,
    )
    workspace_board_section.save()
    return workspace_board_section
