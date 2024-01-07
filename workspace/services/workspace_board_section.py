# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Copyright (C) 2023 JWP Consulting GK
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""Workspace board section services."""
from typing import Optional

from django.db import transaction

from projectify.lib.auth import validate_perm
from user.models import User
from workspace.models import WorkspaceBoard, WorkspaceBoardSection


# Create
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


# Update
def workspace_board_section_update(
    *,
    who: User,
    workspace_board_section: WorkspaceBoardSection,
    title: str,
    description: Optional[str],
) -> WorkspaceBoardSection:
    """Update a workspace board section."""
    validate_perm(
        "workspace.can_update_workspace_board_section",
        who,
        workspace_board_section,
    )
    workspace_board_section.title = title
    workspace_board_section.description = description
    workspace_board_section.save()
    return workspace_board_section


# Delete
@transaction.atomic
def workspace_board_section_delete(
    *,
    who: User,
    workspace_board_section: WorkspaceBoardSection,
) -> None:
    """Delete a workspace board section."""
    validate_perm(
        "workspace.can_delete_workspace_board_section",
        who,
        workspace_board_section,
    )
    workspace_board_section.delete()


# RPC
@transaction.atomic
def workspace_board_section_move(
    *,
    workspace_board_section: WorkspaceBoardSection,
    order: int,
    who: User,
) -> None:
    """
    Move to specified order n within workspace board.

    No save required.
    """
    validate_perm(
        "workspace.can_update_workspace_board_section",
        who,
        workspace_board_section,
    )
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
