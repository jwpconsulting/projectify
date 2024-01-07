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
"""
Workspace services.

This is where all workspace related services will live in the future.
"""
from typing import Optional

from django.contrib.auth.models import (
    AbstractBaseUser,
)

from corporate.services.customer import customer_create
from projectify.lib.auth import validate_perm
from user.models import User
from workspace.models.workspace import (
    Workspace,
)
from workspace.models.workspace_user import (
    WorkspaceUser,
)


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
    return workspace.workspaceuser_set.create(user=user, role=role)
