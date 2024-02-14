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
"""Test WorkspaceUserInvite services."""
import pytest
from rest_framework import serializers

from projectify.user.models import User
from projectify.user.services.internal import user_create
from projectify.workspace.models.workspace import Workspace
from projectify.workspace.models.workspace_user import WorkspaceUser
from projectify.workspace.services.workspace_user_invite import (
    add_or_invite_workspace_user,
    uninvite_user,
)

from ...exceptions import (
    UserAlreadyAdded,
    UserAlreadyInvited,
)


@pytest.mark.django_db
class TestAddOrInviteWorkspaceUser:
    """Test add_or_invite_workspace_user."""

    # We could probably use a more specific type for mailoutbox
    def test_invite_user(
        self,
        workspace: Workspace,
        mailoutbox: list[object],
        workspace_user: WorkspaceUser,
    ) -> None:
        """Test inviting a user."""
        workspace_user_invite = add_or_invite_workspace_user(
            who=workspace_user.user,
            workspace=workspace,
            email_or_user="hello@example.com",
        )
        assert workspace_user_invite.workspace == workspace
        assert len(mailoutbox) == 1

    def test_invite_then_up(
        self,
        workspace: Workspace,
        workspace_user: WorkspaceUser,
    ) -> None:
        """Test inviting with a sign up."""
        count = workspace.users.count()
        add_or_invite_workspace_user(
            who=workspace_user.user,
            workspace=workspace,
            email_or_user="hello@example.com",
        )
        assert workspace.users.count() == count
        user_create(email="hello@example.com")
        assert workspace.users.count() == count + 1

    def test_signs_up_twice(
        self,
        workspace: Workspace,
        workspace_user: WorkspaceUser,
    ) -> None:
        """Test what happens if a user signs up twice."""
        count = workspace.users.count()
        add_or_invite_workspace_user(
            who=workspace_user.user,
            workspace=workspace,
            email_or_user="hello@example.com",
        )
        user = user_create(email="hello@example.com")
        assert workspace.users.count() == count + 1
        user.delete()
        assert workspace.users.count() == count
        user = user_create(email="hello@example.com")
        # The user is not automatically added
        assert workspace.users.count() == count

    def test_inviting_twice(
        self, workspace: Workspace, workspace_user: WorkspaceUser
    ) -> None:
        """Test that inviting twice won't work."""
        add_or_invite_workspace_user(
            who=workspace_user.user,
            workspace=workspace,
            email_or_user="hello@example.com",
        )
        with pytest.raises(UserAlreadyInvited):
            add_or_invite_workspace_user(
                who=workspace_user.user,
                workspace=workspace,
                email_or_user="hello@example.com",
            )

    def test_inviting_workspace_user(
        self, workspace: Workspace, workspace_user: WorkspaceUser
    ) -> None:
        """Test that inviting a pre-existing user won't work."""
        with pytest.raises(UserAlreadyAdded):
            add_or_invite_workspace_user(
                workspace=workspace,
                who=workspace_user.user,
                email_or_user=workspace_user.user.email,
            )

    def test_inviting_user(
        self,
        workspace: Workspace,
        unrelated_user: User,
        workspace_user: WorkspaceUser,
    ) -> None:
        """Test that inviting an existing user will work."""
        count = workspace.workspaceuser_set.count()
        add_or_invite_workspace_user(
            workspace=workspace,
            who=workspace_user.user,
            email_or_user=unrelated_user.email,
        )
        assert workspace.workspaceuser_set.count() == count + 1

    def test_uninviting_user(
        self, workspace_user: WorkspaceUser, workspace: Workspace
    ) -> None:
        """Test uninviting a user."""
        count = workspace.workspaceuserinvite_set.count()
        add_or_invite_workspace_user(
            who=workspace_user.user,
            workspace=workspace,
            email_or_user="hello@example.com",
        )
        assert workspace.workspaceuserinvite_set.count() == count + 1
        uninvite_user(
            workspace=workspace,
            who=workspace_user.user,
            email="hello@example.com",
        )
        assert workspace.workspaceuserinvite_set.count() == count

    def test_after_uninvite(
        self,
        workspace: Workspace,
        workspace_user: WorkspaceUser,
    ) -> None:
        """Test what happens when a user is uninvited."""
        count = workspace.users.count()
        add_or_invite_workspace_user(
            who=workspace_user.user,
            workspace=workspace,
            email_or_user="hello@example.com",
        )
        assert workspace.users.count() == count
        uninvite_user(
            who=workspace_user.user,
            workspace=workspace,
            email="hello@example.com",
        )
        user_create(email="hello@example.com")
        # The user is not added
        assert workspace.users.count() == count

    def test_uninviting_user_on_no_invite(
        self, workspace_user: WorkspaceUser, workspace: Workspace
    ) -> None:
        """Test uninviting a user that was never invited."""
        count = workspace.workspaceuserinvite_set.count()
        with pytest.raises(serializers.ValidationError) as error:
            uninvite_user(
                workspace=workspace,
                who=workspace_user.user,
                email="hello@example.com",
            )
        assert error.match("was never invited")
        assert workspace.workspaceuserinvite_set.count() == count
