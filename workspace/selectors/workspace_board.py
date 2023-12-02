"""Workspace board model selectors."""
from typing import Optional
from uuid import UUID

from user.models import User
from workspace.models.workspace_board import (
    WorkspaceBoard,
    WorkspaceBoardQuerySet,
)


def workspace_board_find_by_workspace_uuid(
    *, workspace_uuid: UUID, who: User, archived: Optional[bool]
) -> WorkspaceBoardQuerySet:
    """Find workspace boards for a workspace."""
    qs = WorkspaceBoard.objects.filter_by_user(who)
    if archived is not None:
        qs = qs.filter_by_archived(archived)
    qs = qs.filter(workspace__uuid=workspace_uuid)
    return qs


def workspace_board_find_by_workspace_board_uuid(
    *, workspace_board_uuid: UUID, who: User
) -> Optional[WorkspaceBoard]:
    """Find a workspace by uuid for a given user."""
    try:
        return WorkspaceBoard.objects.filter_for_user_and_uuid(
            user=who, uuid=workspace_board_uuid
        ).get()
    except WorkspaceBoard.DoesNotExist:
        return None