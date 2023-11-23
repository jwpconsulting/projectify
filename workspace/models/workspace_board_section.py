"""Workspace board section model."""
import uuid
from datetime import (
    datetime,
)
from typing import (
    TYPE_CHECKING,
    Callable,
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

from django_extensions.db.models import (
    TimeStampedModel,
    TitleDescriptionModel,
)

from .task import (
    Task,
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

    from . import WorkspaceBoard  # noqa: F401


class WorkspaceBoardSectionQuerySet(models.QuerySet["WorkspaceBoardSection"]):
    """QuerySet for WorkspaceBoard."""

    def filter_by_workspace_board_pks(self, keys: Pks) -> Self:
        """Filter by workspace boards."""
        return self.filter(workspace_board__pk__in=keys)

    def filter_for_user_and_uuid(
        self, user: AbstractBaseUser, uuid: uuid.UUID
    ) -> Self:
        """Return a workspace for user and uuid."""
        return self.filter(workspace_board__workspace__users=user, uuid=uuid)


class WorkspaceBoardSection(
    TitleDescriptionModel,
    TimeStampedModel,
    models.Model,
):
    """Section of a WorkspaceBoard."""

    workspace_board = models.ForeignKey["WorkspaceBoard"](
        "WorkspaceBoard",
        on_delete=models.CASCADE,
    )
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    objects: ClassVar[WorkspaceBoardSectionQuerySet] = cast(  # type: ignore[assignment]
        WorkspaceBoardSectionQuerySet,
        WorkspaceBoardSectionQuerySet.as_manager(),
    )

    if TYPE_CHECKING:
        # Related managers
        task_set: RelatedManager["Task"]

        # For ordering
        get_task_order: GetOrder
        set_task_order: SetOrder
        get_next_in_order: Callable[[], "WorkspaceBoardSection"]
        _order: int

    def add_task(
        self, title: str, description: str, deadline: Optional[datetime] = None
    ) -> "Task":
        """Add a task to this section."""
        task: Task = self.task_set.create(
            title=title,
            description=description,
            deadline=deadline,
            workspace=self.workspace_board.workspace,
        )
        return task

    def move_to(self, order: int) -> None:
        """
        Move to specified order n within workspace board.

        No save required.
        """
        neighbor_sections = (
            self.workspace_board.workspaceboardsection_set.select_for_update()
        )
        with transaction.atomic():
            # Force queryset to be evaluated to lock them for the time of
            # this transaction
            len(neighbor_sections)
            current_workspace_board = self.workspace_board
            # Django docs wrong, need to cast to list
            order_list = list(
                current_workspace_board.get_workspaceboardsection_order()
            )
            # The list is ordered by pk, which is not uuid for us
            current_object_index = order_list.index(self.pk)
            # Mutate to perform move operation
            order_list.insert(order, order_list.pop(current_object_index))
            # Set new order
            current_workspace_board.set_workspaceboardsection_order(order_list)
            current_workspace_board.save()

    @property
    def workspace(self) -> Workspace:
        """Get workspace instance."""
        return self.workspace_board.workspace

    class Meta:
        """Meta."""

        order_with_respect_to = "workspace_board"
        constraints = [
            models.UniqueConstraint(
                fields=["workspace_board", "_order"],
                name="unique_workspace_board_order",
                deferrable=models.Deferrable.DEFERRED,
            )
        ]
