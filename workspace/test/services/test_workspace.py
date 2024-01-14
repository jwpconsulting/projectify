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
"""Test workspace services."""
import pytest
from faker import Faker
from rest_framework.exceptions import ValidationError

from user.models.user import User
from workspace.models.workspace import Workspace
from workspace.models.workspace_board import WorkspaceBoard
from workspace.models.workspace_user import WorkspaceUser
from workspace.services.workspace import workspace_delete
from workspace.services.workspace_board import workspace_board_delete
from workspace.services.workspace_user import workspace_user_delete
from workspace.services.workspace_user_invite import (
    add_or_invite_workspace_user,
    uninvite_user,
)

pytestmark = pytest.mark.django_db


def test_workspace_delete(
    workspace: Workspace,
    user: User,
) -> None:
    """Test that a freshly created workspace from a fixture can be deleted."""
    count = Workspace.objects.count()
    workspace_delete(workspace=workspace, who=user)
    assert Workspace.objects.count() == count - 1


def test_workspace_delete_dependencies(
    workspace: Workspace,
    workspace_board: WorkspaceBoard,
    other_workspace_user: WorkspaceUser,
    user: User,
    faker: Faker,
) -> None:
    """Test that a freshly created workspace from a fixture can be deleted."""
    count = Workspace.objects.count()

    invite_email = faker.email()
    add_or_invite_workspace_user(
        who=user,
        workspace=workspace,
        email_or_user=invite_email,
    )

    with pytest.raises(ValidationError) as error:
        workspace_delete(workspace=workspace, who=user)
    assert error.match("one remaining workspace user")
    workspace_user_delete(workspace_user=other_workspace_user, who=user)

    with pytest.raises(ValidationError) as error:
        workspace_delete(workspace=workspace, who=user)
    assert error.match("no outstanding invites")

    uninvite_user(who=user, email=invite_email, workspace=workspace)

    with pytest.raises(ValidationError) as error:
        workspace_delete(workspace=workspace, who=user)
    assert error.match("no workspace boards")

    # Finally it will work
    workspace_board_delete(who=user, workspace_board=workspace_board)
    workspace_delete(workspace=workspace, who=user)
    assert Workspace.objects.count() == count - 1
