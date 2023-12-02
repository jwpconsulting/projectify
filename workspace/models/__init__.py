"""Workspace models."""
from typing import (
    ClassVar,
    Self,
    cast,
)

from django.db import (
    models,
)

from .chat_message import ChatMessage, ChatMessageQuerySet
from .const import (
    WorkspaceUserRoles,
)
from .label import (
    Label,
)
from .sub_task import (
    SubTask,
)
from .task import (
    Task,
    TaskQuerySet,
)
from .types import Pks
from .workspace import (
    Workspace,
    WorkspaceQuerySet,
)
from .workspace_board import WorkspaceBoard, WorkspaceBoardQuerySet
from .workspace_board_section import (
    WorkspaceBoardSection,
    WorkspaceBoardSectionQuerySet,
)
from .workspace_user import (
    WorkspaceUser,
)
from .workspace_user_invite import (
    WorkspaceUserInvite,
)


# TODO put me into workspace/models/task_label.py
class TaskLabelQuerySet(models.QuerySet["TaskLabel"]):
    """QuerySet for TaskLabel."""

    def filter_by_task_pks(self, pks: Pks) -> Self:
        """Filter by task pks."""
        return self.filter(task__pk__in=pks)


# TODO put me into workspace/models/task_label.py
class TaskLabel(models.Model):
    """A label to task assignment."""

    task = models.ForeignKey["Task"](
        Task,
        on_delete=models.CASCADE,
    )
    label = models.ForeignKey["Label"](
        Label,
        on_delete=models.CASCADE,
    )

    objects: ClassVar[TaskLabelQuerySet] = cast(  # type: ignore[assignment]
        TaskLabelQuerySet, TaskLabelQuerySet.as_manager()
    )

    @property
    def workspace(self) -> Workspace:
        """Get workspace instance."""
        return self.label.workspace

    class Meta:
        """Meta."""

        unique_together = ("task", "label")


# TODO get rid of trunk export
__all__ = (
    "ChatMessage",
    "ChatMessageQuerySet",
    "Label",
    "SubTask",
    "Task",
    "TaskQuerySet",
    "Workspace",
    "WorkspaceBoard",
    "WorkspaceBoardQuerySet",
    "WorkspaceBoardSection",
    "WorkspaceBoardSectionQuerySet",
    "WorkspaceQuerySet",
    "WorkspaceUser",
    "WorkspaceUserInvite",
    "WorkspaceUserRoles",
)
