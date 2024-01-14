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
from django.db.models.signals import (
    post_delete,
    post_save,
)
from django.dispatch import (
    receiver,
)

from user.signal_defs import (
    user_invitation_redeemed,
)
from workspace.models.label import Label
from workspace.models.task import Task
from workspace.models.workspace import Workspace
from workspace.models.workspace_board import WorkspaceBoard
from workspace.models.workspace_user import WorkspaceUser
from workspace.models.workspace_user_invite import WorkspaceUserInvite
from workspace.services.signals import (
    send_task_change_signal,
    send_workspace_board_change_signal,
    send_workspace_change_signal,
)
from workspace.services.workspace import (
    workspace_add_user,
)

from . import (
    signal_defs,
)

if TYPE_CHECKING:
    from user.models import (  # noqa: F401
        User,
    )


Unknown = object


logger = logging.getLogger(__name__)


@receiver(signal_defs.workspace_user_invited)
def send_invitation_email(instance: WorkspaceUser, **kwargs: object) -> None:
    """Send email when workspace user is invited."""
    # Avoid circular import
    from . import (
        emails,
    )

    email = emails.WorkspaceUserInviteEmail(instance)
    email.send()


@receiver(post_save, sender=Workspace)
@receiver(post_delete, sender=Workspace)
def workspace_changed(instance: Workspace, **kwargs: Unknown) -> None:
    """Broadcast changes upon workspace save/delete."""
    send_workspace_change_signal(instance)


@receiver(post_save, sender=Label)
@receiver(post_delete, sender=Label)
def label_changed(instance: Label, **kwargs: Unknown) -> None:
    """Broadcast changes upon label save/delete."""
    send_workspace_change_signal(instance)


@receiver(post_save, sender=WorkspaceUser)
@receiver(post_delete, sender=WorkspaceUser)
def workspace_user_changed(instance: WorkspaceUser, **kwargs: Unknown) -> None:
    """Broadcast changes upon workspace user save/delete."""
    send_workspace_change_signal(instance)


@receiver(post_save, sender=WorkspaceBoard)
@receiver(post_delete, sender=WorkspaceBoard)
def workspace_board_changed(
    instance: WorkspaceBoard, **kwargs: Unknown
) -> None:
    """Broadcast changes upon workspace board save/delete."""
    send_workspace_board_change_signal(instance)
    send_workspace_change_signal(instance)


@receiver(post_save, sender=Task)
@receiver(post_delete, sender=Task)
def task_changed(instance: Task, **kwargs: Unknown) -> None:
    """Broadcast changes upon task save/delete."""
    send_workspace_board_change_signal(instance)
    send_task_change_signal(instance)


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
