"""Task label model."""
from typing import (
    ClassVar,
    Self,
    cast,
)

from django.db import (
    models,
)

from .label import (
    Label,
)
from .task import (
    Task,
)
from .types import Pks
from .workspace import (
    Workspace,
)


class TaskLabelQuerySet(models.QuerySet["TaskLabel"]):
    """QuerySet for TaskLabel."""

    def filter_by_task_pks(self, pks: Pks) -> Self:
        """Filter by task pks."""
        return self.filter(task__pk__in=pks)


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
