# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2021-2026 JWP Consulting GK
"""Workspace models."""

import uuid

from django.db import models

from projectify.lib.models import BaseModel

from .const import TeamMemberRoles
from .label import Label
from .project import Project
from .section import Section
from .sub_task import SubTask
from .task import Task
from .task_label import TaskLabel
from .team_member import TeamMember
from .team_member_invite import TeamMemberInvite
from .workspace import Workspace


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


__all__ = (
    "ChatMessage",
    "Label",
    "Project",
    "Section",
    "SubTask",
    "Task",
    "TaskLabel",
    "TeamMember",
    "TeamMemberInvite",
    "TeamMemberRoles",
    "Workspace",
)
