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
"""Test WorkspaceUser model."""

import pytest

from user.models import User
from workspace.models.workspace import (
    Workspace,
)
from workspace.services.workspace import (
    workspace_add_user,
)

from ... import (
    models,
)
from ...models import (
    WorkspaceUser,
    WorkspaceUserRoles,
)


@pytest.mark.django_db
class TestWorkspaceUserManager:
    """Test workspace user manager."""

    def test_filter_by_workspace_pks(
        self, workspace_user: WorkspaceUser, workspace: models.Workspace
    ) -> None:
        """Test filter_by_workspace_pks."""
        qs = WorkspaceUser.objects.filter_by_workspace_pks(
            [workspace.pk],
        )
        assert list(qs) == [workspace_user]

    def test_filter_by_user(self, workspace_user: WorkspaceUser) -> None:
        """Test filter_by_user."""
        assert (
            WorkspaceUser.objects.filter_by_user(workspace_user.user).count()
            == 1
        )

    # TODO make me a selector
    def test_filter_by_user_with_unrelated_workspace_user(
        self,
        workspace: Workspace,
        workspace_user: WorkspaceUser,
        unrelated_user: User,
    ) -> None:
        """Test filtering when an unrelated workspace user exists."""
        assert (
            WorkspaceUser.objects.filter_by_user(workspace_user.user).count()
            == 1
        )
        assert (
            WorkspaceUser.objects.filter_by_user(
                unrelated_user,
            ).count()
            == 0
        )
        workspace_add_user(workspace=workspace, user=unrelated_user)
        assert (
            WorkspaceUser.objects.filter_by_user(unrelated_user).count() == 2
        )


@pytest.mark.django_db
class TestWorkspaceUser:
    """Test WorkspaceUser."""

    def test_factory(self, workspace_user: WorkspaceUser) -> None:
        """Test that the default rule is observer."""
        assert workspace_user.role == WorkspaceUserRoles.OWNER

    def test_assign_role(self, workspace_user: WorkspaceUser) -> None:
        """Test assign_role."""
        workspace_user.assign_role(WorkspaceUserRoles.OWNER)
        workspace_user.refresh_from_db()
        assert workspace_user.role == WorkspaceUserRoles.OWNER
