"""Workspace model selectors."""
from typing import Optional
from uuid import UUID

from user.models import User
from workspace.models.workspace import Workspace


def workspace_find_by_workspace_uuid(
    *, workspace_uuid: UUID, who: User
) -> Optional[Workspace]:
    """Find a workspace by uuid for a given user."""
    try:
        return Workspace.objects.filter_for_user_and_uuid(
            user=who, uuid=workspace_uuid
        ).get()
    except Workspace.DoesNotExist:
        return None
