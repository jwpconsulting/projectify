# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2021-2026 JWP Consulting GK
"""Workspace models."""

import uuid
from typing import TYPE_CHECKING

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from projectify.lib.models import BaseModel

from .const import TeamMemberRoles
from .label import Label
from .project import Project
from .section import Section
from .sub_task import SubTask
from .task import Task
from .team_member_invite import TeamMemberInvite
from .workspace import Workspace

if TYPE_CHECKING:
    from django.db.models.fields.related import RelatedField  # noqa: F401
    from django.db.models.manager import RelatedManager  # noqa: F401

    from projectify.user.models import User, UserInvite  # noqa: F401


class TeamMember(BaseModel):
    """Workspace to user mapping."""

    workspace = models.ForeignKey["Workspace"](
        Workspace,
        on_delete=models.PROTECT,
    )
    user = models.ForeignKey["User"](
        # This defo depends on the User in user/ app
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    role = models.CharField(
        max_length=11,
        choices=TeamMemberRoles.choices,
        default=TeamMemberRoles.OBSERVER,
    )
    job_title = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    last_visited_project = models.ForeignKey(
        Project,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text=_(
            "Last project visited by this team member in this workspace"
        ),
    )
    last_visited_workspace = models.DateTimeField(
        null=True,
        blank=True,
        help_text=_(
            "Timestamp when this team member last visited this workspace"
        ),
    )
    minimized_project_list = models.BooleanField(
        default=False,
        help_text=_(
            "Whether this team member has minimized the project list in this workspace"
        ),
    )
    minimized_team_member_filter = models.BooleanField(
        default=False,
        help_text=_(
            "Whether this team member has minimized the team member filter in this workspace"
        ),
    )
    minimized_label_filter = models.BooleanField(
        default=False,
        help_text=_(
            "Whether this team member has minimized the label filter in this workspace"
        ),
    )

    if TYPE_CHECKING:
        # Related
        user_invite: RelatedField[None, "UserInvite"]
        task_set: RelatedManager["Task"]

    def __str__(self) -> str:
        """Return title."""
        return str(self.user)

    class Meta:
        """Meta."""

        unique_together = ("workspace", "user")
        ordering = ("created",)


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
