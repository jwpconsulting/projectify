# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023 JWP Consulting GK
"""Section services."""

from typing import Literal, Optional

from django.db import transaction

from projectify.lib.auth import validate_perm
from projectify.user.models import User
from projectify.workspace.models import Project, Section
from projectify.workspace.services.signals import send_change_signal


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
    section = Section(title=title, description=description, project=project)
    section.save()
    send_change_signal("changed", project)
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
    send_change_signal("changed", section.project)
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
    send_change_signal("changed", section.project)


@transaction.atomic
def section_move_in_direction(
    *, who: User, section: Section, direction: Literal["up", "down"]
) -> None:
    """Move a section up or down within its project."""
    validate_perm("workspace.update_section", who, section.project.workspace)
    match direction:
        case "up":
            if section._order > 0:
                section_move(
                    section=section, who=who, order=section._order - 1
                )
        case "down":
            section_move(section=section, who=who, order=section._order + 1)


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
    send_change_signal("changed", section.project)
