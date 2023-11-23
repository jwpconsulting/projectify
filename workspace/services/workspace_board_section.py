"""Workspace board section services."""

from typing import Optional

from django.db import transaction

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


@transaction.atomic
def workspace_board_section_move(
    *, workspace_board_section: WorkspaceBoardSection, order: int
) -> None:
    """
    Move to specified order n within workspace board.

    No save required.
    """
    workspace_board = workspace_board_section.workspace_board
    neighbor_sections = (
        workspace_board.workspaceboardsection_set.select_for_update()
    )
    # Force queryset to be evaluated to lock them for the time of
    # this transaction
    len(neighbor_sections)
    # Django docs wrong, need to cast to list
    order_list = list(workspace_board.get_workspaceboardsection_order())
    # The list is ordered by pk, which is not uuid for us
    current_object_index = order_list.index(workspace_board_section.pk)
    # Mutate to perform move operation
    order_list.insert(order, order_list.pop(current_object_index))
    # Set new order
    workspace_board.set_workspaceboardsection_order(order_list)
    workspace_board.save()