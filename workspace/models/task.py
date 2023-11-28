"""Contains task model / qs / manager."""
import logging
import uuid
from typing import (
    TYPE_CHECKING,
    Any,
    ClassVar,
    Optional,
    Self,
    cast,
)

from django.contrib.auth.models import (
    AbstractBaseUser,
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
    TimeStampedModel,
    TitleDescriptionModel,
)

from .types import (
    GetOrder,
    Pks,
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
        SubTask,
        TaskLabel,
        WorkspaceBoard,
        WorkspaceBoardSection,
        WorkspaceUser,
    )


class TaskQuerySet(models.QuerySet["Task"]):
    """Manager for Task."""

    def filter_by_workspace(self, workspace: Workspace) -> Self:
        """Filter by workspace."""
        return self.filter(
            workspace_board_section__workspace_board__workspace=workspace,
        )

    def filter_by_assignee(self, assignee: "WorkspaceUser") -> Self:
        """Filter by assignee user."""
        return self.filter(assignee=assignee)

    def filter_by_workspace_board_section_pks(
        self,
        workspace_board_section_pks: Pks,
    ) -> Self:
        """Filter by workspace board section pks."""
        return self.filter(
            workspace_board_section__pk__in=workspace_board_section_pks,
        )

    def filter_by_workspace_board(
        self, workspace_board: "WorkspaceBoard"
    ) -> Self:
        """Filter by tasks contained in workspace board."""
        return self.filter(
            workspace_board_section__workspace_board=workspace_board,
        )

    def filter_for_user_and_uuid(
        self, user: AbstractBaseUser, uuid: uuid.UUID
    ) -> Self:
        """Return task from user workspace corresponding to uuid."""
        return self.filter(
            workspace_board_section__workspace_board__workspace__users=user,
            uuid=uuid,
        )

    # XXX still used?
    def duplicate_task(self, task: "Task") -> "Task":
        """Duplicate a task."""
        new_task = self.create(
            workspace_board_section=task.workspace_board_section,
            title=task.title,
            description=task.description,
            workspace=task.workspace,
        )
        return new_task


@pgtrigger.register(
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
                INNER JOIN "workspace_workspaceboard"
                    ON ("workspace_workspace"."id" = \
                    "workspace_workspaceboard"."workspace_id")
                INNER JOIN "workspace_workspaceboardsection"
                    ON ("workspace_workspaceboard"."id" = \
                         "workspace_workspaceboardsection"."workspace_board_id")
                INNER JOIN "workspace_task"
                    ON ("workspace_workspaceboardsection"."id" = \
                        "workspace_task"."workspace_board_section_id")
                WHERE "workspace_task"."id" = NEW.id
                LIMIT 1;
                IF correct_workspace_id != NEW.workspace_id THEN
                    RAISE EXCEPTION 'invalid workspace_id: workspace being \
                        inserted does not match correct derived workspace.';
                END IF;
                RETURN NEW;
              END;""",
    )
)
@pgtrigger.register(
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
    )
)
class Task(
    TitleDescriptionModel,
    TimeStampedModel,
    models.Model,
):
    """Task, belongs to workspace board section."""

    workspace = models.ForeignKey[Workspace](
        Workspace,
        on_delete=models.CASCADE,
    )

    workspace_board_section = models.ForeignKey["WorkspaceBoardSection"](
        "WorkspaceBoardSection",
        on_delete=models.CASCADE,
    )
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    assignee = models.ForeignKey["WorkspaceUser"](
        "WorkspaceUser",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text=_("Workspace user this task is assigned to."),
    )
    deadline = models.DateTimeField(
        null=True,
        blank=True,
        help_text=_("Task's deadline"),
    )
    labels = models.ManyToManyField(
        "workspace.Label",
        through="workspace.TaskLabel",
    )  # type: models.ManyToManyField["Label", "TaskLabel"]

    number = models.PositiveIntegerField()

    objects: ClassVar[TaskQuerySet] = cast(  # type: ignore[assignment]
        TaskQuerySet, TaskQuerySet.as_manager()
    )

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

    def assign_to(self, assignee: Optional["WorkspaceUser"]) -> None:
        """
        Assign task to user.

        Saves after done.
        """
        # XXX I suppose we can use a database trigger for validation here!
        if assignee:
            self.workspace.workspaceuser_set.get(uuid=assignee.uuid)
        self.assignee = assignee
        self.save()

    def get_next_section(self) -> "WorkspaceBoardSection":
        """Return instance of the next section."""
        next_section: "WorkspaceBoardSection" = (
            self.workspace_board_section.get_next_in_order()
        )
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

        workspace = self.workspace_board_section.workspace_board.workspace

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

    class Meta:
        """Meta."""

        order_with_respect_to = "workspace_board_section"
        constraints = [
            models.UniqueConstraint(
                fields=["workspace_board_section", "_order"],
                name="unique_task_order",
                deferrable=models.Deferrable.DEFERRED,
            ),
            models.UniqueConstraint(
                fields=["workspace", "number"],
                name="unique_task_number",
                deferrable=models.Deferrable.DEFERRED,
            ),
        ]
