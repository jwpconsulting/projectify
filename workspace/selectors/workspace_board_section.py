"""Workspace board section selectors."""
from typing import Optional
from uuid import UUID

from user.models import User
from workspace.models.workspace_board_section import WorkspaceBoardSection


def find_workspace_board_section_for_user_and_uuid(
    *,
    workspace_board_section_uuid: UUID,
    user: User,
) -> Optional[WorkspaceBoardSection]:
    """Find a workspace board section given a UUId and a user."""
    return WorkspaceBoardSection.objects.filter_for_user_and_uuid(
        user=user,
        uuid=workspace_board_section_uuid,
    ).get()
