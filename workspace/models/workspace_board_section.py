"""Workspace board section model."""
import uuid
from typing import (
    TYPE_CHECKING,
    Callable,
    ClassVar,
    Self,
    cast,
)

from django.contrib.auth.models import (
    AbstractBaseUser,
)
from django.db import (
    models,
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
