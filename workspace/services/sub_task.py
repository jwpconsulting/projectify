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
"""Sub task services."""
from typing import NotRequired, Optional, TypedDict
from uuid import UUID

from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from projectify.lib.auth import validate_perm
from user.models import User
from workspace.models.sub_task import SubTask
from workspace.models.task import Task


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

    create_sub_tasks: Optional[list[ValidatedDatum]]
    # TODO
    # If we are really fancy, we could make update_sub_tasks a dict[str,
    # UpdateSubTaskDatum] ??
    update_sub_tasks: Optional[list[ValidatedDatumWithUuid]]


def sub_task_create(
    *,
    who: User,
    task: Task,
    title: str,
    done: bool,
    description: Optional[str] = None,
) -> SubTask:
    """Create a sub task for a task."""
    validate_perm("workspace.can_create_sub_task", who, task)
    return SubTask.objects.create(
        task=task, title=title, description=description, done=done
    )


def sub_task_create_many(
    *,
    who: User,
    task: Task,
    validated_data: ValidatedData,
) -> list[SubTask]:
    """Create several sub tasks."""
    validate_perm("workspace.can_create_sub_task", who, task)
    create_sub_tasks = validated_data["create_sub_tasks"]
    if create_sub_tasks is None:
        raise serializers.ValidationError(
            _("No creatable sub tasks have been provided")
        )
    sub_tasks: list[SubTask] = SubTask.objects.bulk_create(
        SubTask(task=task, **sub_task) for sub_task in create_sub_tasks
    )
    return sub_tasks
