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
"""Workspace user services."""
from typing import Optional

from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from projectify.lib.auth import validate_perm
from user.models import User
from workspace.models.workspace_user import WorkspaceUser
from workspace.services.signals import send_workspace_change_signal


# TODO atomic
def workspace_user_update(
    *,
    workspace_user: WorkspaceUser,
    who: User,
    job_title: Optional[str] = None,
    # TODO should be an enum value
    role: str,
) -> WorkspaceUser:
    """Update a workspace user with new role and job title."""
    validate_perm("workspace.can_update_workspace_user", who, workspace_user)
    workspace_user.job_title = job_title
    workspace_user.role = role
    workspace_user.save()
    send_workspace_change_signal(workspace_user.workspace)
    return workspace_user


# TODO atomic
def workspace_user_delete(
    *,
    workspace_user: WorkspaceUser,
    who: User,
) -> None:
    """
    Delete a workspace user.

    Validate that own user can not be deleted.

    We do not support deleting one's own workspace user for now. This is
    to avoid that if a user is an admin, that they will leave the workspace
    inoperable.

    On the other hand, we might introduce a proper hand-off procedure,
    so big TODO maybe?
    """
    validate_perm("workspace.can_delete_workspace_user", who, workspace_user)
    if workspace_user.user == who:
        raise serializers.ValidationError(
            {"workspace_user": _("Can't delete own workspace user")}
        )
    workspace_user.delete()
    send_workspace_change_signal(workspace_user.workspace)
