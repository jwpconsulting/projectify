"""Contains workspace user invite qs / manager / model."""
from typing import (
    TYPE_CHECKING,
    ClassVar,
    Self,
    cast,
)

from django.db import (
    models,
)
from django.utils.translation import gettext_lazy as _

from projectify.lib.models import BaseModel

from .types import (
    Pks,
)

if TYPE_CHECKING:
    from user.models import UserInvite  # noqa: F401
    from workspace.models import Workspace  # noqa: F401


class WorkspaceUserInviteQuerySet(models.QuerySet["WorkspaceUserInvite"]):
    """QuerySet for WorkspaceUserInvite."""

    def filter_by_workspace_pks(self, workspace_pks: Pks) -> Self:
        """Filter by workspace pks."""
        return self.filter(workspace__pk__in=workspace_pks)

    def filter_by_redeemed(self, redeemed: bool = True) -> Self:
        """Filter by redeemed workspace user invites."""
        return self.filter(redeemed=redeemed)


class WorkspaceUserInvite(BaseModel):
    """UserInvites belonging to this workspace."""

    user_invite = models.ForeignKey["UserInvite"](
        "user.UserInvite",
        on_delete=models.CASCADE,
    )
    workspace = models.ForeignKey["Workspace"](
        "Workspace",
        on_delete=models.CASCADE,
    )
    redeemed = models.BooleanField(
        default=False,
        help_text=_("Has this invite been redeemed?"),
    )

    objects: ClassVar[WorkspaceUserInviteQuerySet] = cast(  # type: ignore[assignment]
        WorkspaceUserInviteQuerySet, WorkspaceUserInviteQuerySet.as_manager()
    )

    def redeem(self) -> None:
        """
        Redeem invite.

        Save.
        """
        assert not self.redeemed
        self.redeemed = True
        self.save()

    class Meta:
        """Meta."""

        unique_together = ("user_invite", "workspace")
