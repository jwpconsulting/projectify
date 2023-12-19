"""Workspace model selectors."""
from typing import Optional
from uuid import UUID

from django.db.models import Prefetch

from user.models import User
from workspace.models.workspace import Workspace, WorkspaceQuerySet
from workspace.models.workspace_board import WorkspaceBoard
from workspace.models.workspace_user import WorkspaceUser

WorkspaceDetailQuerySet = Workspace.objects.prefetch_related(
    "label_set",
).prefetch_related(
    Prefetch(
        "workspaceboard_set",
        queryset=WorkspaceBoard.objects.filter_by_archived(False),
    ),
    Prefetch(
        "workspaceuser_set",
        queryset=WorkspaceUser.objects.select_related(
            "user",
        ),
    ),
)

# 2023-11-30
# I am torn between requiring selectors to select for a user or not
# I don't want to accidentally leak data


def workspace_find_by_workspace_uuid(
    *,
    workspace_uuid: UUID,
    who: User,
    qs: Optional[WorkspaceQuerySet] = None,
) -> Optional[Workspace]:
    """Find a workspace by uuid for a given user."""
    if qs is None:
        qs = Workspace.objects.all()
    try:
        return qs.filter_for_user_and_uuid(user=who, uuid=workspace_uuid).get()
    except Workspace.DoesNotExist:
        return None
