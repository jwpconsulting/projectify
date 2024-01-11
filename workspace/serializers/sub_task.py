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
"""Custom serializer behaviors for sub task."""
from collections.abc import (
    Sequence,
)
from typing import (
    Any,
    NotRequired,
    Optional,
    TypedDict,
)
from uuid import (
    UUID,
)

from django.utils.translation import gettext_lazy as _

from rest_framework import (
    serializers,
)

from workspace.serializers.base import (
    TaskBaseSerializer,
)

from .. import (
    models,
)
from ..models import (
    SubTask,
)


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


class SubTaskListSerializer(serializers.ListSerializer[SubTask]):
    """
    Override sub task list behavior.

    This supports two cases:
    - UUID is given -> Update a given sub task by that uuid
    - UUID not given -> Create a new sub task by that uuid

    Also, adjust the order of sub tasks given by the order of appearance within
    the list.

    Allow restricting sub task selection to only sub tasks from the same task
    by passing task in as a context variable.

    NOTE: Do run this inside a transaction. Validation -> create/update
    depend on each other here, so we can't just wrap each individual method
    in a transaction.atomic.
    """

    validated_data: ValidatedData
    parent: Optional[TaskBaseSerializer]
    _task: Optional[models.Task] = None

    @property
    def task(self) -> Optional[models.Task]:
        """
        Return a task, either by looking inside context or parent.

        Cache the result.
        """
        task: Optional[models.Task]
        if self._task:
            return self._task
        if "task" in self.context:
            task = self.context["task"]
        elif self.parent and self.parent.instance:
            task = self.parent.instance
        else:
            task = None
        self._task = task
        return task

    def to_internal_value(self, data: list[Any]) -> Any:
        """Ensure that we have an instance."""
        if self.instance and self.task:
            raise Exception(
                "You may not provide an instance and a task in the "
                "context simultaneously"
            )
        if self.task and self.instance is None:
            self.instance = list(self.task.subtask_set.all())
        return super().to_internal_value(data)

    def validate(self, validated_data: list[Any]) -> ValidatedData:
        """Ensure that this task has no sub tasks when creating."""
        # We might be creating new sub tasks.
        # 1) determine which sub tasks have to be newly created
        create_sub_tasks: list[ValidatedDatum] = [
            {
                "title": sub_task["title"],
                "description": sub_task.get("description"),
                "done": sub_task["done"],
                "_order": order,
            }
            for order, sub_task in enumerate(validated_data)
            if "uuid" not in sub_task
        ]
        # 2) determine which sub tasks have to be updated
        update_sub_tasks: list[ValidatedDatumWithUuid] = [
            {
                "uuid": sub_task["uuid"],
                "title": sub_task["title"],
                "description": sub_task.get("description"),
                "done": sub_task["done"],
                "_order": order,
            }
            for order, sub_task in enumerate(validated_data)
            if "uuid" in sub_task
        ]
        # 2a) If there are updatable sub tasks, we must have instance data
        if self.instance is None and len(update_sub_tasks):
            raise serializers.ValidationError(
                _(
                    "Sub tasks to be updated have been specified, but no sub "
                    "task instances were provided."
                )
            )
        # 3) check that UUIDs are not duplicated
        unique_uuids = set(sub_task["uuid"] for sub_task in update_sub_tasks)
        if len(unique_uuids) < len(update_sub_tasks):
            raise serializers.ValidationError(
                _("Duplicate UUID found among sub tasks to be updated")
            )
        # 4) check that all update UUIDs are part of instance sub tasks
        #
        # Otherwise, that would mean we are updating a sub task that we did not
        # pass in as an instance. We only need to check this if we are
        # updating. create_sub_tasks by definition can not contain UUIDs
        if self.instance is not None:
            instance_uuids = set(sub_task.uuid for sub_task in self.instance)
            not_contained = unique_uuids - instance_uuids
            if len(not_contained) > 0:
                raise serializers.ValidationError(
                    _(
                        "At least one sub task UUID ({uuid}) could not be "
                        "found amount the instance data. Check whether "
                        "you have correctly passed all task's sub task "
                        "instances."
                    )
                )
        # But: The opposite, a UUID in our update sub task UUIDs not being
        # present does not mean it was forgotten. It means that the sub task
        # shall be deleted in update()
        #
        # 5) Check that when... what was I going to write here?
        return {
            "create_sub_tasks": create_sub_tasks,
            "update_sub_tasks": update_sub_tasks,
        }

    def save(self, **kwargs: Any) -> list[SubTask]:
        """Override save, allow passing complex validated data object."""
        if self.instance is not None:
            self.instance = self.update(self.instance, self.validated_data)
            assert (
                self.instance is not None
            ), "`update()` did not return an object instance."
        else:
            self.instance = self.create(self.validated_data)
            assert (
                self.instance is not None
            ), "`create()` did not return an object instance."
        return self.instance

    def create(
        self, validated_data: ValidatedData, task: Optional[models.Task] = None
    ) -> list[SubTask]:
        """Create several sub tasks."""
        task = self.context.get("task", task)
        if task is None:
            raise ValueError(
                "Task must either be provided as kwarg or in context"
            )
        # XXX select task and sub tasks for update?
        create_sub_tasks = validated_data["create_sub_tasks"]
        if create_sub_tasks is None:
            raise serializers.ValidationError(
                _("No creatable sub tasks have been provided")
            )
        sub_tasks: list[SubTask] = SubTask.objects.bulk_create(
            SubTask(task=task, **sub_task) for sub_task in create_sub_tasks
        )
        return sub_tasks

    def update(
        self,
        instance: Sequence[SubTask],
        validated_data: ValidatedData,
    ) -> list[SubTask]:
        """Update sub tasks."""
        sub_tasks: list[SubTask] = []

        create_sub_tasks = validated_data["create_sub_tasks"]
        update_sub_tasks = validated_data["update_sub_tasks"]

        # 1) delete missing sub tasks
        existing_sub_task_uuids = set(sub_task.uuid for sub_task in instance)
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
                sub_task.uuid: sub_task for sub_task in instance
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
        # 3) create sub tasks and append to results list
        if create_sub_tasks:
            create_instances: list[SubTask] = [
                SubTask(
                    task=self.task,
                    title=create_sub_task["title"],
                    description=create_sub_task.get("description"),
                    done=create_sub_task["done"],
                    _order=create_sub_task["_order"],
                )
                for create_sub_task in create_sub_tasks
            ]
            SubTask.objects.bulk_create(create_instances)
            sub_tasks += create_instances
        # 4) fix order
        return sub_tasks


class SubTaskCreateUpdateSerializer(serializers.ModelSerializer[SubTask]):
    """A sub task serializer that accepts a missing UUID."""

    uuid = serializers.UUIDField(required=False)

    def validate_uuid(self, value: Optional[UUID]) -> Optional[UUID]:
        """
        Validate that when instance is given, there will be no UUID.

        | instance | value | valid? |
        |       no |    no |     no |
        |       no |   yes |    yes |
        |      yes |    no |    yes |
        |      yes |   yes |     no |

        validity = instance XOR value
        """
        if self.instance is not None and value is None:
            raise serializers.ValidationError(
                _("Must specify UUID when updating a sub task")
            )
        # XXX instance isn't always given, so the following code will not work
        # :(
        # if self.instance is None and value is not None:
        #     # raise serializers.ValidationError(
        #     raise serializers.ValidationError(
        #         _("Can't specify UUID when creating a sub task")
        #     )
        return value

    def create(
        self,
        validated_data: dict[str, Any],
        task: Optional[models.Task] = None,
    ) -> SubTask:
        """Forbid create."""
        raise NotImplementedError("Can't call this function anymore")

    class Meta:
        """Use the modified ListSerializer."""

        model = SubTask
        list_serializer_class = SubTaskListSerializer
        fields = (
            "uuid",
            "title",
            "description",
            "done",
        )
