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
from projectify.workspace.models import Section, Project
from projectify.workspace.services.signals import (
    send_project_change_signal,
)


# Create
# TODO make atomic
def section_create(
    *,
    who: User,
    title: str,
    description: Optional[str] = None,
    project: Project,
) -> Section:
    """Create a section."""
    validate_perm(
        "workspace.create_section",
        who,
        project.workspace,
    )
    section = Section(
        title=title,
        description=description,
        project=project,
    )
    section.save()
    send_project_change_signal(project)
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
        section.project.workspace,
    )
    section.title = title
    section.description = description
    section.save()
    send_project_change_signal(section.project)
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
        section.project.workspace,
    )
    section.delete()
    send_project_change_signal(section.project)


# RPC
@transaction.atomic
def section_move(
    *,
    section: Section,
    order: int,
    who: User,
) -> None:
    """
    Move to specified order n within project.

    No save required.
    """
    validate_perm(
        "workspace.update_section",
        who,
        section.project.workspace,
    )
    project = section.project
    neighbor_sections = project.section_set.select_for_update()
    # Force queryset to be evaluated to lock them for the time of
    # this transaction
    len(neighbor_sections)
    # Django docs wrong, need to cast to list
    order_list = list(project.get_section_order())
    # The list is ordered by pk, which is not uuid for us
    current_object_index = order_list.index(section.pk)
    # Mutate to perform move operation
    order_list.insert(order, order_list.pop(current_object_index))
    # Set new order
    project.set_section_order(order_list)
    project.save()
    send_project_change_signal(section.project)
