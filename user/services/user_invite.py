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

from user import signal_defs
from user.models import User, UserInvite
from user.selectors.user import user_find_by_email


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


def user_invite_redeem(*, user_invite: UserInvite, user: User) -> None:
    """Redeem a UserInvite."""
    assert not user_invite.redeemed
    user_invite.redeemed = True
    user_invite.user = user
    user_invite.save()
    signal_defs.user_invitation_redeemed.send(
        sender=user_invite.__class__,
        user=user,
        instance=user_invite,
    )


@transaction.atomic
def user_invite_redeem_many(*, user: User) -> None:
    """Redeem all invites for a user."""
    invites = UserInvite.objects.is_redeemed(False).by_email(user.email)
    for invitation in invites.iterator():
        user_invite_redeem(user_invite=invitation, user=user)
