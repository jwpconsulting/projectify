"""Contains task model / qs / manager."""
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


if TYPE_CHECKING:
    from django.db.models.manager import RelatedManager  # noqa: F401
    from . import (
        ChatMessage,
        WorkspaceUser,
        WorkspaceBoard,
        SubTask,
        TaskLabel,
        Label,
        WorkspaceBoardSection,
    )

from django.db import (
    models,
    transaction,
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

    def move_to(
        self, workspace_board_section: "WorkspaceBoardSection", order: int
    ) -> None:
        """
        Move to specified workspace board section and to order n.

        No save required.
        """
        neighbor_tasks = (
            self.workspace_board_section.task_set.select_for_update()
        )
        if self.workspace_board_section != workspace_board_section:
            other_tasks = workspace_board_section.task_set.select_for_update()
        else:
            # Same section, so no need to select other tasks
            other_tasks = None
        with transaction.atomic():
            # Force both querysets to be evaluated to lock them for the time of
            # this transaction
            len(neighbor_tasks)
            if other_tasks:
                len(other_tasks)
            # Set new WorkspaceBoardSection
            if self.workspace_board_section != workspace_board_section:
                self.workspace_board_section = workspace_board_section
                self.save()

            # Change order
            order_list = list(workspace_board_section.get_task_order())
            current_object_index = order_list.index(self.pk)
            order_list.insert(order, order_list.pop(current_object_index))

            # Set the order
            workspace_board_section.set_task_order(order_list)
            workspace_board_section.save()

    def add_sub_task(self, title: str, description: str) -> "SubTask":
        """Add a sub task."""
        return self.subtask_set.create(title=title, description=description)

    def add_chat_message(
        self, text: str, author: AbstractBaseUser
    ) -> "ChatMessage":
        """Add a chat message."""
        from . import (
            WorkspaceUser,
        )

        workspace_user = WorkspaceUser.objects.get_by_workspace_and_user(
            self.workspace,
            author,
        )
        return self.chatmessage_set.create(text=text, author=workspace_user)

    def assign_to(self, assignee: Optional[AbstractBaseUser]) -> None:
        """
        Assign task to user.

        Saves after done.
        """
        from . import (
            WorkspaceUser,
        )

        if assignee is not None:
            # Check if assignee is part of the task's workspace
            workspace = self.workspace_board_section.workspace_board.workspace
            workspace_user = WorkspaceUser.objects.get_by_workspace_and_user(
                workspace,
                assignee,
            )
        else:
            workspace_user = None
        # Change assignee
        self.assignee = workspace_user
        # Save
        self.save()

    def get_next_section(self) -> "WorkspaceBoardSection":
        """Return instance of the next section."""
        next_section: "WorkspaceBoardSection" = (
            self.workspace_board_section.get_next_in_order()
        )
        return next_section

    def add_label(self, label: "Label") -> "TaskLabel":
        """
        Add a label to this task.

        Returns task label.
        """
        task_label: TaskLabel
        workspace = self.workspace_board_section.workspace_board.workspace
        # XXX can this be a db constraint?
        assert label.workspace == workspace
        with transaction.atomic():
            if self.tasklabel_set.filter(label=label).exists():
                task_label = self.tasklabel_set.get(label=label)
                return task_label
            task_label = self.tasklabel_set.create(label=label)
            return task_label

    def remove_label(self, label: "Label") -> "Label":
        """
        Remove a label from this task. Is idempotent.

        Returns label.
        """
        from . import (
            TaskLabel,
        )

        try:
            task_label: "TaskLabel" = self.tasklabel_set.get(label=label)
            task_label.delete()
        except TaskLabel.DoesNotExist:
            pass
        return label

    # TODO we can probably do better than any here
    def save(self, *args: Any, **kwargs: Any) -> None:
        """Override save to add task number."""
        if self.number is None:
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
