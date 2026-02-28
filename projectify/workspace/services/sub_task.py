# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023-2024 JWP Consulting GK
"""Sub task services."""

from typing import NotRequired, Optional, Sequence, TypedDict
from uuid import UUID

from django.db import transaction

from projectify.lib.auth import validate_perm
from projectify.user.models import User

from ..models import SubTask, Task


class ValidatedDatum(TypedDict):
    """A validated datum, i.e. a single sub task."""

    title: str
    description: NotRequired[str]
    done: bool
    _order: int


class ValidatedDatumWithUuid(ValidatedDatum):
    """A validated datum with UUID required."""

    uuid: UUID


class ValidatedData(TypedDict):
    """Validated data, split by create and update sub tasks."""

    create_sub_tasks: Optional[Sequence[ValidatedDatum]]
    # TODO
    # If we are really fancy, we could make update_sub_tasks a dict[str,
    # UpdateSubTaskDatum] ??
    update_sub_tasks: Optional[Sequence[ValidatedDatumWithUuid]]


@transaction.atomic
def sub_task_create(
    *,
    who: User,
    task: Task,
    title: str,
    done: bool,
    description: Optional[str] = None,
) -> SubTask:
    """Create a sub task for a task."""
    validate_perm("workspace.create_sub_task", who, task.workspace)
    sub_task = SubTask.objects.create(
        task=task, title=title, description=description, done=done
    )
    return sub_task


# The following two functions can be merged into one
@transaction.atomic
def sub_task_create_many(
    *,
    who: User,
    task: Task,
    create_sub_tasks: Sequence[ValidatedDatum],
) -> list[SubTask]:
    """Create several sub tasks."""
    validate_perm("workspace.create_sub_task", who, task.workspace)
    sub_tasks: list[SubTask] = SubTask.objects.bulk_create(
        SubTask(task=task, **sub_task) for sub_task in create_sub_tasks
    )
    return sub_tasks


@transaction.atomic
def sub_task_update_many(
    *,
    who: User,
    task: Task,
    # XXX should be derived from task itself
    sub_tasks: Sequence[SubTask],
    create_sub_tasks: Sequence[ValidatedDatum],
    update_sub_tasks: Sequence[ValidatedDatumWithUuid],
) -> list[SubTask]:
    """Update sub tasks, create missing sub tasks."""
    validate_perm("workspace.create_sub_task", who, task.workspace)
    validate_perm("workspace.update_sub_task", who, task.workspace)
    result: list[SubTask] = []

    # 1) delete missing sub tasks
    existing_sub_task_uuids = set(sub_task.uuid for sub_task in sub_tasks)
    update_sub_tasks_uuids = set(
        sub_task.get("uuid") for sub_task in update_sub_tasks or []
    )
    # All the existing sub task uuids that are not in update sub task uuids
    sub_tasks_to_delete = existing_sub_task_uuids - update_sub_tasks_uuids

    deleted, _ = SubTask.objects.filter(
        # XXX check if uuid is indexed
        uuid__in=sub_tasks_to_delete
    ).delete()

    # Check for consistency after deletion
    if not deleted == len(sub_tasks_to_delete):
        raise Exception("Not all sub tasks were deleted")

    # 2) update sub tasks and append to results list
    if update_sub_tasks:
        sub_task_mapping: dict[UUID, SubTask] = {
            sub_task.uuid: sub_task for sub_task in sub_tasks
        }
        update_instances: list[SubTask] = []
        for sub_task in update_sub_tasks:
            current_instance = sub_task_mapping[sub_task["uuid"]]
            current_instance.title = sub_task["title"]
            current_instance.description = sub_task.get("description")
            current_instance.done = sub_task["done"]
            # pyright doesn't like this one here:
            current_instance._order = sub_task["_order"]
            update_instances.append(current_instance)
        SubTask.objects.bulk_update(
            update_instances,
            ("title", "description", "done", "_order"),
        )
        result += update_instances
    # 3) create sub tasks and append to results list
    if create_sub_tasks:
        create_instances: list[SubTask] = [
            SubTask(
                task=task,
                title=create_sub_task["title"],
                description=create_sub_task.get("description"),
                done=create_sub_task["done"],
                _order=create_sub_task["_order"],
            )
            for create_sub_task in create_sub_tasks
        ]
        SubTask.objects.bulk_create(create_instances)
        result += create_instances
    # 4) fix order
    # XXX ? is fix order missing?
    return result
