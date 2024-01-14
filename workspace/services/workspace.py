# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Copyright (C) 2023-2024 JWP Consulting GK
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
"""
Workspace services.

This is where all workspace related services will live in the future.
"""
import logging
from typing import Optional

from django.contrib.auth.models import (
    AbstractBaseUser,
)
from django.db import transaction
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from corporate.services.customer import customer_create
from projectify.lib.auth import validate_perm
from user.models import User
from workspace.models.workspace import (
    Workspace,
)
from workspace.models.workspace_user import (
    WorkspaceUser,
)
from workspace.services.signals import send_workspace_change_signal

logger = logging.getLogger(__name__)


# Create
def workspace_create(
    *,
    title: str,
    description: Optional[str] = None,
    owner: User,
) -> Workspace:
    """Create a workspace."""
    # TODO validate that user can only create 1 unpaid workspace
    # TODO use Workspace.objects.create
    workspace = Workspace(title=title, description=description)
    workspace.save()
    workspace_add_user(workspace=workspace, user=owner, role="OWNER")
    customer_create(
        who=owner,
        workspace=workspace,
        # TODO not sure if this is good or not. Every workspace starts as a
        # trial workspace with 2 seats.
        seats=2,
    )
    return workspace


# Update
def workspace_update(
    *,
    workspace: Workspace,
    title: str,
    description: Optional[str] = None,
    who: User,
) -> Workspace:
    """Update a workspace."""
    validate_perm(
        "workspace.can_update_workspace",
        who,
        workspace,
    )
    workspace.title = title
    workspace.description = description
    workspace.save()
    return workspace


# Delete
@transaction.atomic
def workspace_delete(
    *,
    who: User,
    workspace: Workspace,
) -> None:
    """
    Delete a workspace.

    The business rules for deleting workspaces haven't really been thought out
    so far, so it will only work under the following conditions:

    - 1 remaining workspace user
    - No open invites
    - No boards
    - No labels
    """
    validate_perm("workspace.can_delete_workspace", who, workspace)
    if workspace.workspaceuser_set.count() > 1:
        raise serializers.ValidationError(
            _("Can only delete workspace with one remaining workspace user")
        )
    if workspace.workspaceuserinvite_set.exists():
        raise serializers.ValidationError(
            _("Can only delete workspace with no outstanding invites")
        )
    if workspace.workspaceboard_set.exists():
        raise serializers.ValidationError(
            _("Can only delete workspace with no workspace boards")
        )
    count, _info = workspace.workspaceuser_set.all().delete()
    logger.info(
        "Deleting workspace %s, after having deleted %d users",
        workspace,
        count,
    )
    workspace.delete()


# TODO looks like this is a private method only to be used to create the
# initial user
def workspace_add_user(
    *,
    workspace: Workspace,
    user: AbstractBaseUser,
    # TODO derive the correct role from an enum
    # Can we just use WorkspaceUserRoles here?
    role: str = "OBSERVER",
) -> WorkspaceUser:
    """Add user to workspace. Return new workspace user."""
    workspace_user = workspace.workspaceuser_set.create(user=user, role=role)
    send_workspace_change_signal(workspace)
    return workspace_user
