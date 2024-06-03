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
"""Contains task model / qs / manager."""
import logging
import uuid
from typing import (
    TYPE_CHECKING,
    Any,
    Optional,
    cast,
)

from django.db import (
    models,
    transaction,
)
from django.db.models.signals import (
    post_save,
)
from django.utils.translation import gettext_lazy as _

import pgtrigger
from django_extensions.db.models import (
    TitleDescriptionModel,
)

from projectify.lib.models import BaseModel

from .types import (
    GetOrder,
    SetOrder,
)
from .workspace import (
    Workspace,
)

logger = logging.getLogger(__name__)


if TYPE_CHECKING:
    from django.db.models.manager import RelatedManager  # noqa: F401

    from . import (
        ChatMessage,
        Label,
        Section,
        SubTask,
        TaskLabel,
        TeamMember,
    )


class Task(TitleDescriptionModel, BaseModel):
    """Task, belongs to section."""

    workspace = models.ForeignKey[Workspace](
        Workspace,
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

    def assign_to(self, assignee: Optional["TeamMember"]) -> None:
        """
        Assign task to user.

        Saves after done.
        """
        # XXX I suppose we can use a database trigger for validation here!
        if assignee:
            self.workspace.teammember_set.get(uuid=assignee.uuid)
        self.assignee = assignee
        self.save()

    def get_next_section(self) -> "Section":
        """Return instance of the next section."""
        next_section: "Section" = self.section.get_next_in_order()
        return next_section

    def set_labels(self, labels: list["Label"]) -> None:
        """Set labels. Remove if unset."""
        workspace = self.workspace
        ws_labels = workspace.label_set
        # We filter for labels as part of this workspace, to make sure we
        # don't assign labels from another workspace
        intersection_qs = ws_labels.filter(
            id__in=[label.id for label in labels]
        )
        with transaction.atomic():
            intersection = list(intersection_qs)
            if not len(intersection) == len(labels):
                logger.warning(
                    "Some of the labels specified in %s are "
                    "not part of this workspace",
                    ", ".join(str(label.uuid) for label in labels),
                )
            self.labels.set(intersection)

        # TODO maybe it makes more sense to fire signals from serializers,
        # not manually patch things like the following...
        # 2023-11-28: Now that I have a lot of success refactoring into
        # services, this should be handled in a service
        post_save.send(sender=Task, instance=self)

    # TODO refactor into service
    def add_label(self, label: "Label") -> "TaskLabel":
        """
        Add a label to this task.

        Returns task label.
        """
        from . import (
            TaskLabel,
        )

        workspace = self.section.project.workspace

        # XXX can this be a db constraint?
        # Or done in the serializer?
        assert label.workspace == workspace

        current_labels = self.labels.all()
        this_label = self.tasklabel_set.filter(label=label)

        with transaction.atomic():
            try:
                return this_label.get()
            except TaskLabel.DoesNotExist:
                self.set_labels([*current_labels, label])
                return self.tasklabel_set.get(label=label)

    def remove_label(self, label: "Label") -> "Label":
        """
        Remove a label from this task. Is idempotent.

        Returns label.
        """
        labels_without = list(self.labels.exclude(id=label.id))

        with transaction.atomic():
            self.set_labels(labels_without)

        return label

    # TODO we can probably do better than any here
    def save(self, *args: Any, **kwargs: Any) -> None:
        """Override save to add task number."""
        if cast(Optional[int], self.number) is None:
            self.number = self.workspace.increment_highest_task_number()
        super().save(*args, **kwargs)

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
