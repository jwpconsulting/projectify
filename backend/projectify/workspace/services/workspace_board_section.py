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
"""Section services."""
from typing import Optional

from django.db import transaction

from projectify.lib.auth import validate_perm
from projectify.user.models import User
from projectify.workspace.models import WorkspaceBoard, Section
from projectify.workspace.services.signals import (
    send_workspace_board_change_signal,
)


# Create
# TODO make atomic
def section_create(
    *,
    who: User,
    title: str,
    description: Optional[str] = None,
    workspace_board: WorkspaceBoard,
) -> Section:
    """Create a section."""
    validate_perm(
        "workspace.create_section",
        who,
        workspace_board.workspace,
    )
    section = Section(
        title=title,
        description=description,
        workspace_board=workspace_board,
    )
    section.save()
    send_workspace_board_change_signal(workspace_board)
    return section


# Update
# TODO make atomic
def section_update(
    *,
    who: User,
    section: Section,
    title: str,
    description: Optional[str] = None,
) -> Section:
    """Update a section."""
    validate_perm(
        "workspace.update_section",
        who,
        section.workspace_board.workspace,
    )
    section.title = title
    section.description = description
    section.save()
    send_workspace_board_change_signal(section.workspace_board)
    return section


# Delete
@transaction.atomic
def section_delete(
    *,
    who: User,
    section: Section,
) -> None:
    """Delete a section."""
    validate_perm(
        "workspace.delete_section",
        who,
        section.workspace_board.workspace,
    )
    section.delete()
    send_workspace_board_change_signal(section.workspace_board)


# RPC
@transaction.atomic
def section_move(
    *,
    section: Section,
    order: int,
    who: User,
) -> None:
    """
    Move to specified order n within workspace board.

    No save required.
    """
    validate_perm(
        "workspace.update_section",
        who,
        section.workspace_board.workspace,
    )
    workspace_board = section.workspace_board
    neighbor_sections = (
        workspace_board.section_set.select_for_update()
    )
    # Force queryset to be evaluated to lock them for the time of
    # this transaction
    len(neighbor_sections)
    # Django docs wrong, need to cast to list
    order_list = list(workspace_board.get_section_order())
    # The list is ordered by pk, which is not uuid for us
    current_object_index = order_list.index(section.pk)
    # Mutate to perform move operation
    order_list.insert(order, order_list.pop(current_object_index))
    # Set new order
    workspace_board.set_section_order(order_list)
    workspace_board.save()
    send_workspace_board_change_signal(section.workspace_board)
