"""Workspace board model."""
import uuid
from typing import (
    TYPE_CHECKING,
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
from django.utils.translation import gettext_lazy as _

from django_extensions.db.models import (
    TitleDescriptionModel,
)

from projectify.lib.models import BaseModel

from .types import Pks
from .workspace import (
    Workspace,
)
from .workspace_board_section import (
    WorkspaceBoardSection,
)

# TODO Here we could be using __all__


if TYPE_CHECKING:
    from django.db.models.manager import RelatedManager  # noqa: F401

    from .types import (
        GetOrder,
        SetOrder,
    )


class WorkspaceBoardQuerySet(models.QuerySet["WorkspaceBoard"]):
    """WorkspaceBoard Manager."""

    def filter_by_workspace(self, workspace: Workspace) -> Self:
        """Filter by workspace."""
        return self.filter(workspace=workspace)

    def filter_by_user(self, user: AbstractBaseUser) -> Self:
        """Filter by user."""
        return self.filter(workspace__users=user)

    def filter_by_workspace_pks(self, workspace_pks: Pks) -> Self:
        """Filter by workspace pks."""
        return self.filter(workspace__pk__in=workspace_pks)

    def filter_for_user_and_uuid(
        self, user: AbstractBaseUser, uuid: uuid.UUID
    ) -> Self:
        """Get a workspace baord for user and uuid."""
        return self.filter_by_user(user).filter(uuid=uuid)

    def filter_by_archived(self, archived: bool = True) -> Self:
        """Filter by archived boards."""
        return self.filter(archived__isnull=not archived)


class WorkspaceBoard(TitleDescriptionModel, BaseModel):
    """Workspace board."""

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
    deadline = models.DateTimeField(
        null=True,
        blank=True,
        help_text=_("Workspace board's deadline"),
    )

    objects: ClassVar[WorkspaceBoardQuerySet] = cast(  # type: ignore[assignment]
        WorkspaceBoardQuerySet, WorkspaceBoardQuerySet.as_manager()
    )

    if TYPE_CHECKING:
        # Related managers
        workspaceboardsection_set: RelatedManager["WorkspaceBoardSection"]

        # For ordering
        get_workspaceboardsection_order: GetOrder
        set_workspaceboardsection_order: SetOrder
