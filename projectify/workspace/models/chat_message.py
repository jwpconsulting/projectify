# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023 JWP Consulting GK
"""Chat message model."""

import uuid

from django.db import models

from projectify.lib.models import BaseModel

from .task import Task
from .team_member import TeamMember


class ChatMessage(BaseModel):
    """ChatMessage, belongs to Task."""

    task = models.ForeignKey["Task"](
        Task,
        on_delete=models.CASCADE,
    )
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    text = models.TextField()
    author = models.ForeignKey["TeamMember"](
        TeamMember,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    class Meta:
        """Meta."""

        ordering = ("created",)
