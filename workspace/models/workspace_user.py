"""Workspace user models."""
import uuid
from typing import (
    TYPE_CHECKING,
    ClassVar,
    Self,
    cast,
)

from django.conf import (
    settings,
)
from django.contrib.auth.models import (
    AbstractBaseUser,
)
from django.db import (
    models,
)

from django_extensions.db.models import (
    TimeStampedModel,
)

from .const import (
    WorkspaceUserRoles,
)
from .types import (
    Pks,
)
from .workspace import (
    Workspace,
)


# TODO Here we could be using __all__


if TYPE_CHECKING:
    from django.db.models.fields.related import RelatedField  # noqa: F401

    from user.models import (  # noqa: F401
        User,
        UserInvite,
    )


class WorkspaceUserQuerySet(models.QuerySet["WorkspaceUser"]):
    """Workspace user queryset."""

    def filter_by_workspace_pks(self, workspace_pks: Pks) -> Self:
        """Filter by workspace pks."""
        return self.filter(workspace__pk__in=workspace_pks)

    def filter_by_user(self, user: AbstractBaseUser) -> Self:
        """Filter workspace users based this user's workspaces."""
        return self.filter(workspace__users=user)

    def get_by_workspace_and_user(
        self, workspace: Workspace, user: AbstractBaseUser
    ) -> "WorkspaceUser":
        """Get by workspace and user."""
        return self.get(workspace=workspace, user=user)


class WorkspaceUser(TimeStampedModel, models.Model):
    """Workspace to user mapping."""

    workspace = models.ForeignKey["Workspace"](
        Workspace,
        on_delete=models.PROTECT,
    )
    # This defo depends on the User in user/ app
    user = models.ForeignKey["User"](
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    role = models.CharField(
        max_length=10,
        choices=WorkspaceUserRoles.choices,
        default=WorkspaceUserRoles.OBSERVER,
    )
    job_title = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)

    # Sort of nonsensical
    objects: ClassVar[WorkspaceUserQuerySet] = cast(  # type: ignore[assignment]
        WorkspaceUserQuerySet, WorkspaceUserQuerySet.as_manager()
    )

    if TYPE_CHECKING:
        # Related
        user_invite: RelatedField[None, "UserInvite"]

    def assign_role(self, role: str) -> None:
        """
        Assign a new role.

        Saves.
        """
        self.role = role
        self.save()

    class Meta:
        """Meta."""

        unique_together = ("workspace", "user")
