# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2021-2026 JWP Consulting GK
"""Workspace models."""

import logging
import uuid
from typing import TYPE_CHECKING, Any, Callable, Optional

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

import pgtrigger

from projectify.lib.models import BaseModel, TitleDescriptionModel
from projectify.user.models import UserInvite

from ..types import WorkspaceQuota
from .const import TeamMemberRoles
from .types import GetOrder, SetOrder

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
        upload_to="workspace_picture/",
        blank=True,
        null=True,
    )

    # Optional annotation to show trial limits
    # Since it involves additional queries, it is None by default
    quota: Optional[WorkspaceQuota] = None

    if TYPE_CHECKING:
        # Related fields
        customer: RelatedField[None, "Customer"]

        # Related sets
        project_set: RelatedManager["Project"]
        teammember_set: RelatedManager["TeamMember"]
        teammemberinvite_set: RelatedManager["TeamMemberInvite"]
        label_set: RelatedManager["Label"]
        active_invites: Optional[RelatedManager["TeamMemberInvite"]]

    def __str__(self) -> str:
        """Return title."""
        return self.title

    def refresh_from_db(self, *args: Any, **kwargs: Any) -> None:
        """
        Clear active_invites.

        This is a workaround so that invites get removed after deleting them.
        """
        setattr(self, "active_invites", [])
        super().refresh_from_db(*args, **kwargs)

    class Meta:
        """Add constraints and triggers."""

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


class Label(BaseModel):
    """A label."""

    # TODO It should be fine to just use TitleDescription here
    name = models.CharField(max_length=255)
    """
    0 -> orange
    2 -> pink
    3 -> blue
    4 -> purple
    5 -> yellow
    6 -> red
    7 -> green
    """
    color = models.PositiveBigIntegerField(
        help_text=_("Color index"),
    )
    workspace = models.ForeignKey["Workspace"](
        "Workspace",
        on_delete=models.CASCADE,
    )
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)

    if TYPE_CHECKING:
        id: int

    def save(self, *args: Any, **kwargs: Any) -> None:
        """Override save and call full_clean."""
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        """Return name."""
        return self.name

    class Meta:
        """Meta."""

        ordering = ("-modified",)
        constraints = [
            models.CheckConstraint(
                # type: ignore[call-arg]
                condition=models.Q(color__gte=0) & models.Q(color__lte=7),
                name="label_color_range",
                violation_error_message=_("Color must be between 0 and 7"),
            ),
            models.UniqueConstraint(
                fields=["name", "workspace"],
                name="unique_label_name_per_workspace",
                violation_error_message=_(
                    "You can only create one label with this name."
                ),
            ),
        ]


class Project(TitleDescriptionModel, BaseModel):
    """Project."""

    workspace = models.ForeignKey["Workspace"](
        Workspace,
        on_delete=models.PROTECT,
    )
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    archived = models.DateTimeField(
        null=True,
        blank=True,
        help_text=_("Archival timestamp of this workspace board."),
    )
    due_date = models.DateTimeField(
        null=True,
        blank=True,
        help_text=_("Due date for this workspace board"),
    )

    if TYPE_CHECKING:
        # Related managers
        section_set: RelatedManager["Section"]

        # For ordering
        get_section_order: GetOrder
        set_section_order: SetOrder

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


class Section(TitleDescriptionModel, BaseModel):
    """Section of a Project."""

    project = models.ForeignKey["Project"]("Project", on_delete=models.CASCADE)
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    minimized_by = models.ManyToManyField(
        "user.User",
        blank=True,
        related_name="minimized_sections",
        help_text=_("Users who have minimized this section"),
    )  # type: models.ManyToManyField[User, "Section"]

    if TYPE_CHECKING:
        # Related managers
        task_set: RelatedManager["Task"]

        # For ordering
        get_task_order: GetOrder
        set_task_order: SetOrder
        get_next_in_order: Callable[[], "Section"]
        _order: int

    def __str__(self) -> str:
        """Return title."""
        return self.title

    def get_absolute_url(self) -> str:
        """Get URL to section within project."""
        return f"{reverse('dashboard:projects:detail', args=(str(self.project.uuid),))}#section-{self.uuid}"

    class Meta:
        """Meta."""

        order_with_respect_to = "project"
        constraints = [
            models.UniqueConstraint(
                fields=["project", "_order"],
                name="unique_project_order",
                deferrable=models.Deferrable.DEFERRED,
            )
        ]


class Task(TitleDescriptionModel, BaseModel):
    """Task, belongs to section."""

    workspace = models.ForeignKey["Workspace"](
        "workspace.Workspace",
        on_delete=models.CASCADE,
    )

    section = models.ForeignKey["Section"]("Section", on_delete=models.CASCADE)
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    assignee = models.ForeignKey["TeamMember"](
        "TeamMember",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text=_("Team member this task is assigned to."),
    )
    due_date = models.DateTimeField(
        null=True,
        blank=True,
        help_text=_("Due date for this task"),
    )
    labels = models.ManyToManyField(
        "workspace.Label",
        through="workspace.TaskLabel",
    )  # type: models.ManyToManyField["Label", "TaskLabel"]
    done = models.DateTimeField(null=True, blank=True)

    if TYPE_CHECKING:
        chatmessage_set: RelatedManager["ChatMessage"]
        tasklabel_set: RelatedManager["TaskLabel"]
        _order: int
        id: int

    def __str__(self) -> str:
        """Return title."""
        return self.title

    class Meta:
        """Meta."""

        order_with_respect_to = "section"
        constraints = [
            models.UniqueConstraint(
                fields=["section", "_order"],
                name="unique_task_order",
                deferrable=models.Deferrable.DEFERRED,
            ),
        ]

        triggers = (
            pgtrigger.Trigger(
                name="ensure_correct_workspace",
                when=pgtrigger.Before,
                operation=pgtrigger.Insert | pgtrigger.Update,
                func="""
                      DECLARE
                        correct_workspace_id   INTEGER;
                      BEGIN
                        SELECT "workspace_workspace"."id" INTO correct_workspace_id
                        FROM "workspace_workspace"
                        INNER JOIN "workspace_project"
                            ON ("workspace_workspace"."id" = \
                            "workspace_project"."workspace_id")
                        INNER JOIN "workspace_section"
                            ON ("workspace_project"."id" = \
                                 "workspace_section"."project_id")
                        INNER JOIN "workspace_task"
                            ON ("workspace_section"."id" = \
                                "workspace_task"."section_id")
                        WHERE "workspace_task"."id" = NEW.id
                        LIMIT 1;
                        IF correct_workspace_id != NEW.workspace_id THEN
                            RAISE EXCEPTION 'invalid workspace_id: workspace being \
                                inserted does not match correct derived workspace.';
                        END IF;
                        RETURN NEW;
                      END;""",
            ),
        )


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


class TeamMemberInvite(BaseModel):
    """UserInvites belonging to this workspace."""

    user_invite = models.ForeignKey[UserInvite](
        "user.UserInvite",
        on_delete=models.CASCADE,
    )
    workspace = models.ForeignKey["Workspace"](
        "Workspace",
        on_delete=models.CASCADE,
    )
    # TODO use redeemed_when only
    redeemed = models.BooleanField(
        default=False,
        help_text=_("Has this invite been redeemed?"),
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
        Workspace,
        on_delete=models.PROTECT,
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
