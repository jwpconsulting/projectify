"""Contain workspace model and qs."""
import uuid
from datetime import (
    datetime,
)
from typing import (
    TYPE_CHECKING,
    ClassVar,
    Optional,
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
    transaction,
)
from django.utils.translation import gettext_lazy as _

import pgtrigger
from django_extensions.db.models import (
    TimeStampedModel,
    TitleDescriptionModel,
)
from user import models as user_models

from .. import (
    signal_defs,
)
from .const import (
    MAINTAINER_EQUIVALENT,
    MEMBER_EQUIVALENT,
    OBSERVER_EQUIVALENT,
    OWNER_EQUIVALENT,
    WorkspaceUserRoles,
)
from .workspace_user_invite import (
    WorkspaceUserInvite,
)


if TYPE_CHECKING:
    from django.db.models.fields.related import RelatedField  # noqa: F401
    from django.db.models.manager import RelatedManager  # noqa: F401

    from corporate.models import (
        Customer,
    )

    from . import (
        Label,
        WorkspaceBoard,
        WorkspaceUser,
    )


class WorkspaceQuerySet(models.QuerySet["Workspace"]):
    """Workspace Manager."""

    def get_for_user(self, user: AbstractBaseUser) -> Self:
        """Return workspaces for a user."""
        return self.filter(users=user)

    def filter_for_user_and_uuid(
        self, user: AbstractBaseUser, uuid: uuid.UUID
    ) -> Self:
        """Return workspace for user and uuid."""
        return self.get_for_user(user).filter(uuid=uuid)


@pgtrigger.register(
    pgtrigger.Trigger(
        name="ensure_correct_highest_task_number",
        when=pgtrigger.Before,
        operation=pgtrigger.Update,
        func="""
              DECLARE
                max_task_number   INTEGER;
              BEGIN
                SELECT MAX(workspace_task.number) INTO max_task_number
                FROM workspace_task
                WHERE workspace_task.workspace_id = NEW.id;
                IF NEW.highest_task_number < max_task_number THEN
                    RAISE EXCEPTION 'invalid highest_task_number:  \
                    highest_task_number cannot be lower than a task number.';
                END IF;
                RETURN NEW;
              END;""",
    )
)
class Workspace(TitleDescriptionModel, TimeStampedModel, models.Model):
    """Workspace."""

    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through="WorkspaceUser",
        through_fields=("workspace", "user"),
    )  # type: models.ManyToManyField[AbstractBaseUser, "WorkspaceUser"]
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    picture = models.ImageField(
        upload_to="workspace_picture/",
        blank=True,
        null=True,
    )

    highest_task_number = models.IntegerField(default=0)

    objects: ClassVar[WorkspaceQuerySet] = cast(  # type: ignore[assignment]
        WorkspaceQuerySet, WorkspaceQuerySet.as_manager()
    )

    if TYPE_CHECKING:
        # Related fields
        customer: RelatedField[None, "Customer"]

        # Related sets
        workspaceboard_set: RelatedManager["WorkspaceBoard"]
        workspaceuser_set: RelatedManager["WorkspaceUser"]
        workspaceuserinvite_set: RelatedManager["WorkspaceUserInvite"]
        label_set: RelatedManager["Label"]

    def add_workspace_board(
        self, title: str, description: str, deadline: Optional[datetime] = None
    ) -> "WorkspaceBoard":
        """Add workspace board."""
        workspace_board: "WorkspaceBoard" = self.workspaceboard_set.create(
            title=title,
            description=description,
            deadline=deadline,
        )
        return workspace_board

    def add_user(self, user: AbstractBaseUser) -> AbstractBaseUser:
        """
        Add user to workspace.

        Return user.
        """
        self.workspaceuser_set.create(user=user)
        return user

    # TODO I wish this worked with WorkspaceUser instead?
    @transaction.atomic
    def remove_user(self, user: AbstractBaseUser) -> AbstractBaseUser:
        """
        Remove user from workspace.

        Removes the user from task assignments.

        Return user.
        """
        workspace_user = self.workspaceuser_set.get(user=user)
        workspace_user.delete()
        return user

    @transaction.atomic
    def invite_user(self, email: str) -> "WorkspaceUserInvite":
        """Invite a user to this workspace."""
        invite_check_qs = WorkspaceUserInvite.objects.filter(
            user_invite__email=email,
            workspace=self,
        )
        if invite_check_qs.exists():
            raise ValueError(_("Email is already invited"))
        already_user_qs = self.users.filter(
            email=email,
        )
        if already_user_qs.exists():
            raise ValueError(_("Email is already workspace user"))
        user_invite = user_models.UserInvite.objects.invite_user(email)
        workspace_user_invite: WorkspaceUserInvite = (
            self.workspaceuserinvite_set.create(
                user_invite=user_invite,
                workspace=self,
            )
        )
        signal_defs.workspace_user_invited.send(
            sender=self.__class__,
            instance=workspace_user_invite,
        )
        return workspace_user_invite

    @transaction.atomic
    def uninvite_user(self, email: str) -> None:
        """Remove a users invitation."""
        workspace_user_invite = self.workspaceuserinvite_set.get(
            user_invite__email=email,
        )
        workspace_user_invite.delete()

    @transaction.atomic
    def increment_highest_task_number(self) -> int:
        """
        Increment and return highest task number.

        Atomic.
        """
        qs = Workspace.objects.filter(pk=self.pk).select_for_update()
        qs.update(highest_task_number=models.F("highest_task_number") + 1)
        return qs.get().highest_task_number

    def has_at_least_role(
        self, workspace_user: "WorkspaceUser", role: str
    ) -> bool:
        """Check if a workspace user has at least a given role."""
        if not workspace_user.workspace == self:
            return False
        if role == WorkspaceUserRoles.OBSERVER:
            return workspace_user.role in OBSERVER_EQUIVALENT
        elif role == WorkspaceUserRoles.MEMBER:
            return workspace_user.role in MEMBER_EQUIVALENT
        elif role == WorkspaceUserRoles.MAINTAINER:
            return workspace_user.role in MAINTAINER_EQUIVALENT
        elif role == WorkspaceUserRoles.OWNER:
            return workspace_user.role in OWNER_EQUIVALENT
        else:
            raise ValueError(
                f"This just happened: {workspace_user} {role} {self}"
            )

    @property
    def workspace(self) -> Self:
        """Get workspace instance."""
        return self
