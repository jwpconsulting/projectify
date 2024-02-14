# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Copyright (C) 2023 JWP Consulting GK
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""Workspace user invite services."""
from typing import (
    Optional,
    Union,
)

from django.contrib.auth.models import (
    AbstractBaseUser,
)
from django.db import (
    transaction,
)
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from projectify.lib.auth import (
    validate_perm,
)
from projectify.premail.email import EmailAddress
from projectify.user.models import (  # noqa: F401
    User,
    UserInvite,
)
from projectify.user.services.user_invite import user_invite_create
from projectify.workspace.emails import WorkspaceUserInviteEmail
from projectify.workspace.exceptions import (
    UserAlreadyAdded,
    UserAlreadyInvited,
)
from projectify.workspace.models.workspace import Workspace
from projectify.workspace.models.workspace_user import (
    WorkspaceUser,
)
from projectify.workspace.models.workspace_user_invite import (
    WorkspaceUserInvite,
)
from projectify.workspace.services.workspace import (
    workspace_add_user,
)


# TODO these could be better suited as selectors
def _try_find_workspace_user(
    # TODO add *,
    workspace: Workspace,
    email: str,
) -> Union[None, AbstractBaseUser, WorkspaceUser]:
    """
    Try to find a workspace user by email.

    If not found return just the user.
    If no user found, return None.
    """
    # This part could be in user/selectors/user
    try:
        user = User.objects.get_by_natural_key(email)
    except User.DoesNotExist:
        return None
    try:
        return workspace.workspaceuser_set.get(user=user)
    except WorkspaceUser.DoesNotExist:
        return user


def _try_find_invitation(
    # TODO add *,
    workspace: Workspace,
    email: str,
) -> Union[UserInvite, WorkspaceUserInvite, None]:
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


# TODO rename me workspace_user_invite_create
@transaction.atomic
def add_or_invite_workspace_user(
    *,
    workspace: Workspace,
    email_or_user: Union[AbstractBaseUser, str],
    who: User,
) -> Union[WorkspaceUser, WorkspaceUserInvite]:
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
            return workspace_add_user(workspace=workspace, user=user)
        case email:
            pass

    match _try_find_workspace_user(workspace, email):
        case WorkspaceUser():
            raise UserAlreadyAdded()
        case AbstractBaseUser() as user:
            return workspace_add_user(workspace=workspace, user=user)
        case None:
            pass

    # XXX
    # Turn this back into non-optional
    user_invite: Optional[UserInvite]

    match _try_find_invitation(workspace, email):
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

    email_to_send = WorkspaceUserInviteEmail(
        receiver=EmailAddress(email), obj=workspace_user_invite
    )
    email_to_send.send()

    return workspace_user_invite


# TODO rename me workspace_user_invite_delete
@transaction.atomic
def uninvite_user(who: User, workspace: Workspace, email: str) -> None:
    """Remove a users invitation."""
    validate_perm("workspace.can_delete_workspace_user_invite", who, workspace)
    invite = _try_find_invitation(
        workspace=workspace,
        email=email,
    )
    match invite:
        case UserInvite() | None:
            raise serializers.ValidationError(
                {"email": _("User with this email was never invited")}
            )
        case WorkspaceUserInvite() as workspace_user_invite:
            workspace_user_invite.delete()
