# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2021-2026 JWP Consulting GK
"""Workspace models."""

import logging
import uuid
from typing import TYPE_CHECKING, Any, Callable, Optional, cast

from django.conf import settings
from django.db import models, transaction
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

import pgtrigger

from projectify.lib.models import BaseModel, TitleDescriptionModel
from projectify.user.models import UserInvite

from ..types import WorkspaceQuota
from .const import TeamMemberRoles
from .label import Label
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

    highest_task_number = models.IntegerField(default=0)

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

    @transaction.atomic
    def increment_highest_task_number(self) -> int:
        """
        Increment and return highest task number.

        Atomic.
        """
        qs = Workspace.objects.filter(pk=self.pk).select_for_update()
        qs.update(highest_task_number=models.F("highest_task_number") + 1)
        return qs.get().highest_task_number

    def __str__(self) -> str:
        """Return title."""
        return self.title

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

        triggers = (
            pgtrigger.Trigger(
                name="ensure_correct_highest_task_number",
                when=pgtrigger.Before,
                operation=pgtrigger.Update,
                func="""
              DECLARE
                max_task_number   INTEGER;
              BEGIN
                SELECT MAX(workspace_task.number) INTO max_task_number
                FROM workspace_task
                WHERE workspace_task.workspace_id = NEW.id;
                IF NEW.highest_task_number < max_task_number THEN
                    RAISE EXCEPTION 'invalid highest_task_number:  \
                    highest_task_number cannot be lower than a task number.';
                END IF;
                RETURN NEW;
              END;""",
            ),
        )


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

    number = models.PositiveIntegerField()

    if TYPE_CHECKING:
        # Related fields
        subtask_set: RelatedManager["SubTask"]
        chatmessage_set: RelatedManager["ChatMessage"]
        tasklabel_set: RelatedManager["TaskLabel"]

        # Order related
        get_subtask_order: GetOrder
        set_subtask_order: SetOrder
        _order: int
        id: int

    # TODO we can probably do better than any here
    def save(self, *args: Any, **kwargs: Any) -> None:
        """Override save to add task number."""
        if cast(Optional[int], self.number) is None:
            self.number = self.workspace.increment_highest_task_number()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        """Return title."""
        return self.title

    def readable_number(self) -> str:
        """Return title with number. This is useful for AT."""
        return _("Task number {task_number}").format(task_number=self.number)

    class Meta:
        """Meta."""

        order_with_respect_to = "section"
        constraints = [
            models.UniqueConstraint(
                fields=["section", "_order"],
                name="unique_task_order",
                deferrable=models.Deferrable.DEFERRED,
            ),
            models.UniqueConstraint(
                fields=["workspace", "number"],
                name="unique_task_number",
                deferrable=models.Deferrable.DEFERRED,
            ),
        ]

        triggers = (
            pgtrigger.Trigger(
                name="read_only_task_number",
                when=pgtrigger.Before,
                operation=pgtrigger.Update,
                func="""
              BEGIN
                IF NEW.number != OLD.number THEN
                    RAISE EXCEPTION 'invalid number: Task number \
                        cannot be modified after inserting Task.';
                END IF;
                RETURN NEW;
              END;""",
            ),
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
