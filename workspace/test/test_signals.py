# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Copyright (C) 2022, 2023 JWP Consulting GK
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
"""Test workspace signals."""
# TODO instead of signals, we should just perform the relevant action in
# services

import pytest

from user.services.user import user_create
from workspace.models.workspace_user import WorkspaceUser
from workspace.services.workspace_user_invite import (
    add_or_invite_workspace_user,
    uninvite_user,
)

from .. import (
    models,
)


@pytest.mark.django_db
class TestRedeemWorkspaceInvitations:
    """Test redeem_workspace_invitations."""

    def test_simple(
        self,
        workspace: models.Workspace,
        workspace_user: WorkspaceUser,
    ) -> None:
        """Test simple case."""
        count = workspace.users.count()
        add_or_invite_workspace_user(
            who=workspace_user.user,
            workspace=workspace,
            email_or_user="hello@example.com",
        )
        assert workspace.users.count() == count
        user_create("hello@example.com")
        assert workspace.users.count() == count + 1

    def test_signs_up_twice(
        self,
        workspace: models.Workspace,
        workspace_user: WorkspaceUser,
    ) -> None:
        """Test what happens if a user signs up twice."""
        count = workspace.users.count()
        add_or_invite_workspace_user(
            who=workspace_user.user,
            workspace=workspace,
            email_or_user="hello@example.com",
        )
        user = user_create("hello@example.com")
        assert workspace.users.count() == count + 1
        user.delete()
        assert workspace.users.count() == count
        user = user_create("hello@example.com")
        # The user is not automatically added
        assert workspace.users.count() == count

    def test_after_uninvite(
        self,
        workspace: models.Workspace,
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
        user_create("hello@example.com")
        # The user is not added
        assert workspace.users.count() == count
