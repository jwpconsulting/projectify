# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Copyright (C) 2022-2024 JWP Consulting GK
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
"""Workspace signals."""
import logging
from typing import (
    TYPE_CHECKING,
)

from django.db import (
    transaction,
)
from django.dispatch import (
    receiver,
)

from user.signal_defs import (
    user_invitation_redeemed,
)
from workspace.models.workspace_user_invite import WorkspaceUserInvite
from workspace.services.workspace import (
    workspace_add_user,
)

if TYPE_CHECKING:
    from user.models import (  # noqa: F401
        User,
    )


Unknown = object


logger = logging.getLogger(__name__)


# TODO this should be in services
@receiver(user_invitation_redeemed)
@transaction.atomic
def redeem_workspace_invitations(
    user: "User", instance: WorkspaceUserInvite, **kwargs: Unknown
) -> None:
    """Redeem workspace invitations."""
    qs = WorkspaceUserInvite.objects.filter(
        user_invite__user=user,
    )
    for invite in qs:
        workspace = invite.workspace
        workspace_add_user(workspace=workspace, user=user)
        invite.redeem()
