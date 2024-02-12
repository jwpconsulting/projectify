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
"""Test WorkspaceUserInvite model."""
import pytest

from ... import (
    models,
)


@pytest.mark.django_db
class TestWorkspaceUserInviteQuerySet:
    """Test WorkspaceUserInviteQuerySet."""

    def test_filter_by_workspace_pks(
        self,
        workspace: models.Workspace,
        workspace_user_invite: models.WorkspaceUserInvite,
    ) -> None:
        """Test filter_by_workspace_pks."""
        qs = models.WorkspaceUserInvite.objects.filter_by_workspace_pks(
            [workspace.pk],
        )
        assert list(qs) == [workspace_user_invite]

    def test_filter_by_redeemed(
        self,
        workspace: models.Workspace,
        workspace_user_invite: models.WorkspaceUserInvite,
    ) -> None:
        """Test filter_by_redeemed."""
        qs = models.WorkspaceUserInvite.objects.filter_by_redeemed(False)
        assert qs.count() == 1
        workspace_user_invite.redeem()
        assert qs.count() == 0
        qs = models.WorkspaceUserInvite.objects.filter_by_redeemed(True)
        assert qs.count() == 1


@pytest.mark.django_db
class TestWorkspaceUserInvite:
    """Test workspace user invite."""

    def test_factory(
        self, workspace_user_invite: models.WorkspaceUserInvite
    ) -> None:
        """Test factory."""
        assert workspace_user_invite

    def test_redeem(
        self, workspace_user_invite: models.WorkspaceUserInvite
    ) -> None:
        """Test redeeming."""
        workspace_user_invite.redeem()
        workspace_user_invite.refresh_from_db()
        assert workspace_user_invite.redeemed

    def test_redeeming_twice(
        self, workspace_user_invite: models.WorkspaceUserInvite
    ) -> None:
        """Test redeeming twice."""
        workspace_user_invite.redeem()
        with pytest.raises(AssertionError):
            workspace_user_invite.redeem()
