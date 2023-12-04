"""Contain workspace model and qs."""
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
    transaction,
)

import pgtrigger
from django_extensions.db.models import (
    TimeStampedModel,
    TitleDescriptionModel,
)

from .const import (
    MAINTAINER_EQUIVALENT,
    MEMBER_EQUIVALENT,
    OBSERVER_EQUIVALENT,
    OWNER_EQUIVALENT,
    WorkspaceUserRoles,
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
    from .workspace_user_invite import (
        WorkspaceUserInvite,
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
