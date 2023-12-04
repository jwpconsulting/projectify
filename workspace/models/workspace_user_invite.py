"""Contains workspace user invite qs / manager / model."""
from typing import (
    ClassVar,
    Optional,
    Self,
    Union,
    cast,
)

from django.contrib.auth.models import (
    AbstractBaseUser,
)
from django.db import (
    models,
    transaction,
)
from django.utils.translation import gettext_lazy as _

from django_extensions.db.models import (
    TimeStampedModel,
)

from projectify.utils import (
    get_user_model,
    validate_perm,
)
from user.models import (  # noqa: F401
    User,
    UserInvite,
)
from user.services.user_invite import user_invite_create
from workspace import (
    signal_defs,
)
from workspace.exceptions import (
    UserAlreadyAdded,
    UserAlreadyInvited,
)
from workspace.models.workspace_user import (
    WorkspaceUser,
)
from workspace.services.workspace import (
    workspace_add_user,
)

from .types import (
    Pks,
)
from .workspace import (
    Workspace,
)


class WorkspaceUserInviteQuerySet(models.QuerySet["WorkspaceUserInvite"]):
    """QuerySet for WorkspaceUserInvite."""

    def filter_by_workspace_pks(self, workspace_pks: Pks) -> Self:
        """Filter by workspace pks."""
        return self.filter(workspace__pk__in=workspace_pks)

    def filter_by_redeemed(self, redeemed: bool = True) -> Self:
        """Filter by redeemed workspace user invites."""
        return self.filter(redeemed=redeemed)


class WorkspaceUserInvite(TimeStampedModel, models.Model):
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


# TODO The following methods shall be moved to
# workspace/services/workspace_user_invite.py
def try_find_workspace_user(
    workspace: "Workspace", email: str
) -> Union[None, "AbstractBaseUser", "WorkspaceUser"]:
    """
    Try to find a workspace user by email.

    If not found return just the user.
    If no user found, return None.
    """
    User = get_user_model()
    try:
        user = User.objects.get_by_natural_key(email)
    except User.DoesNotExist:
        return None
    try:
        return workspace.workspaceuser_set.get(user=user)
    except WorkspaceUser.DoesNotExist:
        return user


def try_find_invitation(
    workspace: "Workspace", email: str
) -> Union["UserInvite", WorkspaceUserInvite, None]:
    """
    Try to locate a workspace user invite.

    If not workspace user invite can be found, try to return a user invite.
    If nothing found, return None.
    """
    try:
        user_invite = UserInvite.objects.get(
            email=email,
        )
    except UserInvite.DoesNotExist:
        return None
    try:
        return workspace.workspaceuserinvite_set.get(
            user_invite=user_invite,
        )
    except WorkspaceUserInvite.DoesNotExist:
        return None


@transaction.atomic
def add_or_invite_workspace_user(
    *,
    workspace: "Workspace",
    email_or_user: Union[AbstractBaseUser, str],
    who: User,
) -> Union["WorkspaceUser", "WorkspaceUserInvite"]:
    """
    Add or invite a new workspace user. Accept either email or user instance.

    There are a few scenarios to consider here:
    1) User exists, part of this workspace
    raise UserAlreadyAdded
    2) User exists, not part of this workspace
    Add WorkspaceUser
    3) No user registration, invited to this workspace
    raise UserAlreadyInvited
    4) No user registration, invited to the platform, but not workspace
    Create a WorkspaceUserInvite
    5) No user registration, never invited to this workspace:
    Create a UserInvite and a WorkspaceUserInvite
    """
    validate_perm("workspace.can_create_workspace_user", who, workspace)
    match email_or_user:
        case AbstractBaseUser() as user:
            return workspace_add_user(workspace, user)
        case email:
            pass

    match try_find_workspace_user(workspace, email):
        case WorkspaceUser():
            raise UserAlreadyAdded()
        case AbstractBaseUser() as user:
            return workspace_add_user(workspace, user)
        case None:
            pass

    # XXX
    # Turn this back into non-optional
    user_invite: Optional[UserInvite]

    match try_find_invitation(workspace, email):
        case WorkspaceUserInvite():
            raise UserAlreadyInvited(_("Email is already invited"))
        case UserInvite() as found:
            user_invite = found
        case None:
            user_invite = user_invite_create(email=email)

    # TODO remove me again, we should just be optimistically creating a user
    # invite uncoditonally
    if user_invite is None:
        raise AssertionError("This shouldn't be hit")

    workspace_user_invite: WorkspaceUserInvite = (
        workspace.workspaceuserinvite_set.create(user_invite=user_invite)
    )
    signal_defs.workspace_user_invited.send(
        sender=Workspace,
        instance=workspace_user_invite,
    )
    return workspace_user_invite
