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
"""Custom serializer behaviors for sub task."""
from collections.abc import Sequence
from typing import Any, Optional
from uuid import UUID

from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from ..models import SubTask
from ..models.task import Task
from ..serializers.base import TaskBaseSerializer
from ..services.sub_task import (
    ValidatedData,
)


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
    _task: Optional[Task] = None

    # TODO remove
    @property
    def task(self) -> Optional[Task]:
        """
        Return a task, either by looking inside context or parent.

        Cache the result.
        """
        task: Optional[Task]
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

    # TODO remove
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

    # TODO remove
    def save(self, **kwargs: Any) -> list[SubTask]:
        """Override save, allow passing complex validated data object."""
        del kwargs
        raise NotImplementedError("Do not call")

    # TODO remove
    def create(
        self, validated_data: ValidatedData, task: Optional[Task] = None
    ) -> list[SubTask]:
        """Create several sub tasks."""
        del validated_data
        del task
        raise NotImplementedError("Do not call")

    # TODO remove
    def update(
        self,
        instance: Sequence[SubTask],
        validated_data: ValidatedData,
    ) -> list[SubTask]:
        """Update sub tasks."""
        del instance
        del validated_data
        raise NotImplementedError("Do not call")


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
        task: Optional[Task] = None,
    ) -> SubTask:
        """Forbid create."""
        del validated_data
        del task
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
