# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023-2024 JWP Consulting GK
"""Task services."""

import logging
from datetime import datetime
from typing import Literal, Optional, Sequence, Union

from django.db import transaction
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from projectify.lib.auth import validate_perm
from projectify.user.models import User

from ..models import Label, Section, Task, TeamMember

logger = logging.getLogger(__name__)


# TODO hide this
def task_assign_labels(*, task: Task, labels: Sequence[Label]) -> None:
    """Assign label uuids to the given task."""
    workspace = task.workspace
    ws_labels = workspace.label_set
    # We filter for labels as part of this workspace, to make sure we
    # don't assign labels from another workspace
    intersection_qs = ws_labels.filter(id__in=[label.id for label in labels])
    with transaction.atomic():
        intersection = list(intersection_qs)
        if not len(intersection) == len(labels):
            logger.warning(
                "Some of the labels specified in %s are "
                "not part of this workspace",
                ", ".join(str(label.uuid) for label in labels),
            )
        task.labels.set(intersection)


@transaction.atomic
def task_create(
    *,
    who: User,
    section: Section,
    title: str,
    # TODO make label optional
    labels: Optional[Sequence[Label]] = None,
    description: Optional[str] = None,
    due_date: Optional[datetime] = None,
    assignee: Optional[TeamMember] = None,
) -> Task:
    """Create a task. This will replace the above task_create method."""
    validate_perm(
        "workspace.create_task",
        who,
        section.project.workspace,
    )
    # XXX Implicit N+1 here
    workspace = section.project.workspace
    if assignee and assignee.workspace != workspace:
        raise serializers.ValidationError(
            {
                "assignee": _(
                    "The team member to be assigned belongs to a different workspace"
                )
            }
        )
    task = Task.objects.create(
        section=section,
        title=title,
        description=description,
        due_date=due_date,
        workspace=workspace,
        assignee=assignee,
    )
    if labels is not None:
        task_assign_labels(task=task, labels=labels)
    return task


# Update
@transaction.atomic
def task_update(
    *,
    who: User,
    task: Task,
    title: str,
    description: Optional[str] = None,
    due_date: Optional[datetime] = None,
    assignee: Optional[TeamMember] = None,
    labels: Optional[Sequence[Label]] = None,
) -> Task:
    """Assign labels, assign assignee."""
    validate_perm("workspace.update_task", who, task.workspace)
    task.title = title
    task.description = description
    task.due_date = due_date
    task.assignee = assignee
    task.save()
    if labels is not None:
        task_assign_labels(task=task, labels=labels)
    return task


@transaction.atomic
def task_mark_done(
    *,
    who: User,
    task: Task,
    done: bool,
) -> Task:
    """Assign labels, assign assignee."""
    validate_perm("workspace.update_task", who, task.workspace)
    if done:
        task.done = now()
    else:
        task.done = None
    task.save()
    return task


# Delete
# TODO atomic
def task_delete(*, task: Task, who: User) -> None:
    """Delete a task."""
    validate_perm("workspace.delete_task", who, task.workspace)
    task.delete()


@transaction.atomic
def task_move_in_direction(
    *, who: User, task: Task, direction: Literal["up", "down", "top", "bottom"]
) -> Task:
    """
    Move a task up, down, to top or bottom.

    Uses task_move_after.
    """
    validate_perm("workspace.update_task", who, task.workspace)
    section = task.section
    tasks = section.task_set
    neighbor: Union[Task, Section]
    match direction:
        case "up":
            maybe_neighbor = tasks.filter(_order=task._order - 1)
            if maybe_neighbor.exists():
                neighbor = maybe_neighbor.get()
            else:
                neighbor = section

        case "down":
            maybe_neighbor = tasks.filter(_order=task._order + 1)
            # TODO, maybe we just want to move it to the next section
            if not maybe_neighbor.exists():
                raise ValidationError(
                    _("Can't move task down, there is no next task")
                )
            neighbor = maybe_neighbor.get()

        case "bottom":
            maybe_task = tasks.last()
            if not maybe_task:
                raise RuntimeError(f"There's no task after task {task.uuid}")
            neighbor = maybe_task
        case "top":
            neighbor = section
    return task_move_after(who=who, task=task, after=neighbor)


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
        task.section = section
        task.save()

    # Change order
    order_list = list(section.get_task_order())
    current_object_index = order_list.index(task.pk)
    order_list.insert(order, order_list.pop(current_object_index))

    # Set the order
    section.set_task_order(order_list)
    section.save()
    return task
