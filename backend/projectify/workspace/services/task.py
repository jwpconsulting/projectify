# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Copyright (C) 2023-2024 JWP Consulting GK
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
"""Task services."""
from datetime import datetime
from typing import Optional, Sequence, Union

from django.db import transaction

from projectify.lib.auth import validate_perm
from projectify.user.models import User
from projectify.workspace.models.label import Label
from projectify.workspace.models.section import (
    Section,
)
from projectify.workspace.models.task import Task
from projectify.workspace.models.team_member import TeamMember
from projectify.workspace.services.signals import (
    send_project_change_signal,
    send_task_change_signal,
)
from projectify.workspace.services.sub_task import (
    ValidatedData,
    sub_task_create_many,
    sub_task_update_many,
)


# TODO hide this
def task_assign_labels(*, task: Task, labels: Sequence[Label]) -> None:
    """Assign label uuids to the given task."""
    task.set_labels(list(labels))


# Create
def task_create(
    *,
    who: User,
    section: Section,
    title: str,
    description: Optional[str] = None,
    due_date: Optional[datetime] = None,
    assignee: Optional[TeamMember] = None,
) -> Task:
    """Add a task to this section."""
    validate_perm(
        "workspace.create_task",
        who,
        section.project.workspace,
    )
    # XXX Implicit N+1 here
    workspace = section.project.workspace
    return Task.objects.create(
        workspace_board_section=section,
        title=title,
        description=description,
        due_date=due_date,
        workspace=workspace,
        assignee=assignee,
    )


# TODO make this the regular task_create
@transaction.atomic
def task_create_nested(
    *,
    who: User,
    section: Section,
    title: str,
    # TODO make these two optional as well
    sub_tasks: ValidatedData,
    labels: Sequence[Label],
    description: Optional[str] = None,
    due_date: Optional[datetime] = None,
    assignee: Optional[TeamMember] = None,
) -> Task:
    """Create a task. This will replace the above task_create method."""
    task = task_create(
        who=who,
        section=section,
        title=title,
        description=description,
        assignee=assignee,
        due_date=due_date,
    )
    task_assign_labels(task=task, labels=labels)

    create_sub_tasks = sub_tasks["create_sub_tasks"] or []
    sub_task_create_many(
        who=who,
        task=task,
        create_sub_tasks=create_sub_tasks,
    )
    send_project_change_signal(task.section.project)
    return task


# Update
def task_update(
    *,
    who: User,
    task: Task,
    title: str,
    description: Optional[str] = None,
    due_date: Optional[datetime] = None,
    assignee: Optional[TeamMember] = None,
) -> Task:
    """Add a task to this section."""
    validate_perm("workspace.update_task", who, task.workspace)
    task.title = title
    task.description = description
    task.due_date = due_date
    task.assignee = assignee
    task.save()
    return task


# TODO make this method replace the above task_update
@transaction.atomic
def task_update_nested(
    *,
    who: User,
    task: Task,
    title: str,
    description: Optional[str] = None,
    due_date: Optional[datetime] = None,
    assignee: Optional[TeamMember] = None,
    # Make these two optional
    labels: Sequence[Label],
    sub_tasks: ValidatedData,
) -> Task:
    """Assign labels, assign assignee."""
    task = task_update(
        who=who,
        task=task,
        title=title,
        description=description,
        due_date=due_date,
        assignee=assignee,
    )
    task_assign_labels(task=task, labels=labels)
    sub_task_instances = list(task.subtask_set.all())
    sub_task_update_many(
        task=task,
        who=who,
        sub_tasks=sub_task_instances,
        create_sub_tasks=sub_tasks["create_sub_tasks"] or [],
        update_sub_tasks=sub_tasks["update_sub_tasks"] or [],
    )
    send_project_change_signal(task.section.project)
    send_task_change_signal(task)
    return task


# Delete
# TODO atomic
def task_delete(*, task: Task, who: User) -> None:
    """Delete a task."""
    validate_perm("workspace.delete_task", who, task.workspace)
    task.delete()
    send_project_change_signal(task.section.project)
    send_task_change_signal(task)


@transaction.atomic
def task_move_after(
    *,
    who: User,
    task: Task,
    after: Union[Task, Section],
) -> Task:
    """Move a task after a task or in front of a section."""
    validate_perm("workspace.update_task", who, task.workspace)
    match after:
        case Task():
            section = after.section
            order = after._order
        case Section():
            section = after
            order = 0

    # Lock tasks in own section
    neighbor_tasks = section.task_set.select_for_update()
    len(neighbor_tasks)

    # Depending on whether we move within the same section, we
    # might have to lock only this section, or the destination
    # as well.
    if task.section != section:
        other_tasks = section.task_set.select_for_update()
        len(other_tasks)
        # And assign task's section
        task.workspace_board_section = section
        task.save()

    # Change order
    order_list = list(section.get_task_order())
    current_object_index = order_list.index(task.pk)
    order_list.insert(order, order_list.pop(current_object_index))

    # Set the order
    section.set_task_order(order_list)
    section.save()
    send_project_change_signal(task.section.project)
    send_task_change_signal(task)
    return task
