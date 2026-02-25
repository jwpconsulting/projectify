# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2021, 2022, 2023 JWP Consulting GK
"""Task label model."""

from django.db import models

from projectify.lib.models import BaseModel

from .label import Label
from .task import Task


class TaskLabel(BaseModel):
    """A label to task assignment."""

    task = models.ForeignKey["Task"](
        Task,
        on_delete=models.CASCADE,
    )
    label = models.ForeignKey["Label"](
        Label,
        on_delete=models.CASCADE,
    )

    class Meta:
        """Meta."""

        unique_together = ("task", "label")
