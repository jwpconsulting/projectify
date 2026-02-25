# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023 JWP Consulting GK
"""Contain sub task model and manager."""

import uuid

from django.db import models, transaction
from django.utils.translation import gettext_lazy as _

from projectify.lib.models import BaseModel, TitleDescriptionModel

from .task import Task
from .workspace import Workspace as Workspace


class SubTask(TitleDescriptionModel, BaseModel):
    """SubTask, belongs to Task."""

    task = models.ForeignKey[Task](
        Task,
        on_delete=models.CASCADE,
    )
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    done = models.BooleanField(
        default=False,
        help_text=_("Designate whether this sub task is done"),
    )

    # Ordering related
    _order: int

    def move_to(self, order: int) -> None:
        """
        Move to specified order n within task.

        No save required.
        """
        neighbor_subtasks = self.task.subtask_set.select_for_update()
        with transaction.atomic():
            # Force queryset to be evaluated to lock them for the time of
            # this transaction
            len(neighbor_subtasks)
            current_task = self.task
            # Django docs wrong, need to cast to list
            order_list = list(current_task.get_subtask_order())
            # The list is ordered by pk, which is not uuid for us
            current_object_index = order_list.index(self.pk)
            # Mutate to perform move operation
            order_list.insert(order, order_list.pop(current_object_index))
            # Set new order
            current_task.set_subtask_order(order_list)
            current_task.save()

    class Meta:
        """Meta."""

        order_with_respect_to = "task"
        constraints = [
            models.UniqueConstraint(
                fields=["task", "_order"],
                name="unique_sub_task_order",
                deferrable=models.Deferrable.DEFERRED,
            )
        ]
