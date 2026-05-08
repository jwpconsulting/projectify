# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2021-2026 JWP Consulting GK
"""Workspace models."""

import logging
import uuid
from typing import TYPE_CHECKING, Any, Optional

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import F
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from projectify.lib.models import (
    BaseModel,
    RichTextField,
    TitleDescriptionModel,
)
from projectify.user.models import UserInvite

from .const import TeamMemberRoles
from .types import WorkspaceQuota

if TYPE_CHECKING:
    from django.db.models.fields.related import RelatedField  # noqa: F401
    from django.db.models.manager import RelatedManager  # noqa: F401

    from projectify.corporate.models import Customer
    from projectify.user.models import User, UserInvite  # noqa: F401


logger = logging.getLogger(__name__)


class Workspace(TitleDescriptionModel, BaseModel):
    """Workspace."""

    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through="TeamMember",
        through_fields=("workspace", "user"),
    )  # type: models.ManyToManyField[User, "TeamMember"]
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    picture = models.ImageField(
        upload_to="workspace_picture/", blank=True, null=True
    )

    # Optional annotation to show trial limits
    # Since it involves additional queries, it is None by default
    quota: Optional[WorkspaceQuota] = None

    # Map User primary keys to team member roles
    # This might contain stale roles but only if this object isn't recreated
    role_cache: dict[int, TeamMemberRoles]

    def __init__(self, *args: Any, **kwargs: Any):
        """Create role cache."""
        super().__init__(*args, **kwargs)
        self.role_cache = {}

    if TYPE_CHECKING:
        # Related fields
        customer: RelatedField[None, "Customer"]

        # Related sets
        task_set: RelatedManager["Task"]
        project_set: RelatedManager["Project"]
        teammember_set: RelatedManager["TeamMember"]
        teammemberinvite_set: RelatedManager["TeamMemberInvite"]
        active_invites: Optional[RelatedManager["TeamMemberInvite"]]

    def __str__(self) -> str:
        """Return title."""
        return self.title

    def refresh_from_db(self, *args: Any, **kwargs: Any) -> None:
        """
        Clear active_invites and role_cache.

        This is a workaround so that invites get removed after deleting them.
        """
        setattr(self, "active_invites", [])
        self.role_cache = {}
        super().refresh_from_db(*args, **kwargs)

    class Meta:
        """Add constraints."""

        constraints = (
            models.CheckConstraint(
                name="title",
                # Match period followed by space, or not period
                # type: ignore[call-arg]
                condition=models.Q(title__regex=r"^([.:]\s|[^.:])*[.:]?$"),
                violation_error_message=_(
                    "Workspace title can only contain '.' or ':' if followed "
                    "by whitespace or if located at the end."
                ),
            ),
        )


class Project(TitleDescriptionModel, BaseModel):
    """Project."""

    workspace = models.ForeignKey["Workspace"](
        Workspace, on_delete=models.PROTECT
    )
    description = RichTextField(_("description"), blank=True, null=True)
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    archived = models.DateTimeField(
        null=True,
        blank=True,
        help_text=_("Archival timestamp of this workspace board."),
    )
    due_date = models.DateTimeField(
        null=True, blank=True, help_text=_("Due date for this workspace board")
    )

    if TYPE_CHECKING:
        # Related managers
        task_set: RelatedManager["Task"]

    def __str__(self) -> str:
        """Return title."""
        return self.title

    def get_absolute_url(self) -> str:
        """Return the absolute URL for this project."""
        return reverse(
            "dashboard:projects:detail", kwargs={"project_uuid": self.uuid}
        )

    class Meta:
        """Order by created, descending."""

        ordering = ("-created",)


class Task(TitleDescriptionModel, BaseModel):
    """Task, belongs to project."""

    # Override description and make it a rich text field
    description = RichTextField(_("description"), blank=True, null=True)
    workspace = models.ForeignKey["Workspace"](
        "workspace.Workspace", on_delete=models.CASCADE
    )
    project = models.ForeignKey[Project](Project, on_delete=models.CASCADE)
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    assignee = models.ForeignKey["TeamMember"](
        "TeamMember",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text=_("Team member this task is assigned to."),
    )
    due_date = models.DateTimeField(
        null=True, blank=True, help_text=_("Due date for this task")
    )
    done = models.DateTimeField(null=True, blank=True)

    if TYPE_CHECKING:
        id: int

    def save(self, *args: Any, **kwargs: Any) -> None:
        """Validate workspace == project.workspace."""
        correct_workspace = self.project.workspace
        if self.workspace.pk != correct_workspace.pk:
            raise ValidationError(
                _("Task workspace must match project.workspace").format()
            )
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        """Return title."""
        return self.title

    def get_absolute_url(self) -> str:
        """Return absolute URL to this task."""
        return reverse("dashboard:tasks:detail", args=(self.uuid,))

    class Meta:
        """Meta."""

        # This was originally the following
        # ordering = ("done", "-modified")
        # I've changed it to use these expressions to avoid sorting
        # inconsistencies between local SQLite and PostgreSQL on the
        # www.projectifyapp.com Hetzner instance
        ordering = [F("done").asc(nulls_first=True), F("modified").desc()]


class TeamMemberInvite(BaseModel):
    """UserInvites belonging to this workspace."""

    user_invite = models.ForeignKey[UserInvite](
        "user.UserInvite", on_delete=models.CASCADE
    )
    workspace = models.ForeignKey["Workspace"](
        "Workspace", on_delete=models.CASCADE
    )
    # TODO use redeemed_when only
    redeemed = models.BooleanField(
        default=False, help_text=_("Has this invite been redeemed?")
    )
    redeemed_when = models.DateTimeField(
        blank=True,
        null=True,
        editable=False,
        default=None,
        help_text=_("When has this invite been redeemed?"),
    )

    class Meta:
        """Meta."""

        unique_together = ("user_invite", "workspace")
        ordering = ("created",)


class TeamMember(BaseModel):
    """Workspace to user mapping."""

    workspace = models.ForeignKey["Workspace"](
        Workspace, on_delete=models.PROTECT
    )
    user = models.ForeignKey["User"](
        # This defo depends on the User in user/ app
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    role = models.CharField(
        # XXX why 11?
        max_length=11,
        choices=TeamMemberRoles.choices,
        default=TeamMemberRoles.OBSERVER,
    )
    job_title = models.CharField(max_length=255, null=True, blank=True)
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
    # TODO remove
    minimized_project_list = models.BooleanField(
        default=False,
        help_text=_(
            "Whether this team member has minimized the project list in this workspace"
        ),
    )
    # TODO remove
    minimized_team_member_filter = models.BooleanField(
        default=False,
        help_text=_(
            "Whether this team member has minimized the team member filter in this workspace"
        ),
    )

    if TYPE_CHECKING:
        # Related
        user_invite: RelatedField[None, "UserInvite"]
        task_set: RelatedManager["Task"]
        workspace_id: int

    def __str__(self) -> str:
        """Return title."""
        return str(self.user)

    class Meta:
        """Meta."""

        unique_together = ("workspace", "user")
        ordering = ("created",)


__all__ = (
    "Project",
    # TODO remove
    "Task",
    "TeamMember",
    "TeamMemberInvite",
    "TeamMemberRoles",
    "Workspace",
)
