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
"""User invite services."""

from typing import Optional

from django.db import transaction

from user.models import User, UserInvite
from user.selectors.user import user_find_by_email
from workspace.models.workspace_user_invite import WorkspaceUserInvite
from workspace.services.workspace import workspace_add_user


@transaction.atomic
def user_invite_create(*, email: str) -> Optional[UserInvite]:
    """Invite a user by email address."""
    user = user_find_by_email(email=email)
    if user:
        return None
    # TODO make this a selector
    invite_qs = UserInvite.objects.by_email(email).is_redeemed(False)
    if invite_qs.exists():
        return invite_qs.get()
    return UserInvite.objects.create(email=email)


@transaction.atomic
def user_invite_redeem(*, user_invite: UserInvite, user: User) -> None:
    """Redeem a UserInvite."""
    assert not user_invite.redeemed
    user_invite.redeemed = True
    user_invite.user = user
    user_invite.save()

    # Add user to workspaces for any outstanding invites
    qs = WorkspaceUserInvite.objects.filter(
        user_invite__user=user,
    )
    for invite in qs:
        workspace = invite.workspace
        workspace_add_user(workspace=workspace, user=user)
        invite.redeem()


@transaction.atomic
def user_invite_redeem_many(*, user: User) -> None:
    """Redeem all invites for a user."""
    invites = UserInvite.objects.is_redeemed(False).by_email(user.email)
    for invitation in invites.iterator():
        user_invite_redeem(user_invite=invitation, user=user)
