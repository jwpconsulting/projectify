# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023-2024 JWP Consulting GK
"""Team member invite services."""

from typing import Optional, Union

from django.db import transaction
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from projectify.lib.auth import validate_perm
from projectify.premail.email import EmailAddress
from projectify.user.models import User, UserInvite
from projectify.user.services.user_invite import user_invite_create

from ..emails import TeamMemberInviteEmail
from ..models.const import TeamMemberRoles
from ..models.team_member import TeamMember
from ..models.team_member_invite import TeamMemberInvite
from ..models.workspace import Workspace
from ..services.workspace import workspace_add_user


# TODO these could be better suited as selectors
def _try_find_team_member(
    # TODO add *,
    workspace: Workspace,
    email: str,
) -> Union[None, User, TeamMember]:
    """
    Try to find a team member by email.

    If not found return just the user.
    If no user found, return None.
    """
    # This part could be in user/selectors/user
    try:
        user = User.objects.get_by_natural_key(email)
    except User.DoesNotExist:
        return None
    try:
        return workspace.teammember_set.get(user=user)
    except TeamMember.DoesNotExist:
        return user


def _try_find_invitation(
    # TODO add *,
    workspace: Workspace,
    email: str,
) -> Union[UserInvite, TeamMemberInvite, None]:
    """
    Try to locate a team member invite.

    If not team member invite can be found, try to return a user invite.
    If nothing found, return None.
    """
    try:
        user_invite = UserInvite.objects.get(email=email, redeemed=False)
    except UserInvite.DoesNotExist:
        return None
    try:
        return workspace.teammemberinvite_set.get(
            user_invite=user_invite, redeemed=False
        )
    except TeamMemberInvite.DoesNotExist:
        return None


@transaction.atomic
def team_member_invite_create(
    *,
    workspace: Workspace,
    email_or_user: Union[User, str],
    who: User,
) -> Union[TeamMember, TeamMemberInvite]:
    """
    Add or invite a new team member. Accept either email or user instance.

    There are a few scenarios to consider here:
    1) User exists, part of this workspace
    raise UserAlreadyAdded
    2) User exists, not part of this workspace
    Add TeamMember
    3) No user registration, invited to this workspace
    raise UserAlreadyInvited
    4) No user registration, invited to the platform, but not workspace
    Create a TeamMemberInvite
    5) No user registration, never invited to this workspace:
    Create a UserInvite and a TeamMemberInvite
    """
    validate_perm("workspace.create_team_member", who, workspace)
    match email_or_user:
        case User() as user:
            return workspace_add_user(
                workspace=workspace,
                user=user,
                role=TeamMemberRoles.OBSERVER,
            )
        case email:
            pass

    match _try_find_team_member(workspace, email):
        case TeamMember():
            raise serializers.ValidationError(
                {
                    "email": _(
                        "This user already is a team member in your workspace."
                    ).format(email)
                }
            )
        case User() as user:
            return workspace_add_user(
                workspace=workspace,
                user=user,
                role=TeamMemberRoles.OBSERVER,
            )
        case None:
            pass

    # XXX
    # Turn this back into non-optional
    user_invite: Optional[UserInvite]

    match _try_find_invitation(workspace, email):
        case TeamMemberInvite():
            raise serializers.ValidationError(
                {
                    "email": _(
                        "You've already invited this email address to your workspace."
                    ).format(email)
                }
            )
        case UserInvite() as found:
            user_invite = found
        case None:
            user_invite = user_invite_create(email=email)

    # TODO remove me again, we should just be optimistically creating a user
    # invite uncoditonally
    if user_invite is None:
        raise AssertionError("This shouldn't be hit")

    team_member_invite = TeamMemberInvite.objects.create(
        workspace=workspace, user_invite=user_invite
    )

    email_to_send = TeamMemberInviteEmail(
        receiver=EmailAddress(email),
        obj=team_member_invite,
        who=who,
    )
    email_to_send.send()

    return team_member_invite


@transaction.atomic
def team_member_invite_delete(
    *, who: User, workspace: Workspace, email: str
) -> None:
    """Remove a users invitation."""
    validate_perm("workspace.delete_team_member_invite", who, workspace)
    invite = _try_find_invitation(
        workspace=workspace,
        email=email,
    )
    match invite:
        case UserInvite() | None:
            raise serializers.ValidationError(
                {"email": _("User with this email was never invited")}
            )
        case TeamMemberInvite() as team_member_invite:
            team_member_invite.delete()
