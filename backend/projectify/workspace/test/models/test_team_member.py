# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023 JWP Consulting GK
"""Test TeamMember model."""

import pytest

from projectify.user.models import User

from ...models.const import TeamMemberRoles
from ...models.team_member import TeamMember
from ...models.workspace import Workspace
from ...services.workspace import workspace_add_user


@pytest.mark.django_db
class TestTeamMemberManager:
    """Test team member manager."""

    def test_filter_by_workspace_pks(
        self, team_member: TeamMember, workspace: Workspace
    ) -> None:
        """Test filter_by_workspace_pks."""
        qs = TeamMember.objects.filter_by_workspace_pks(
            [workspace.pk],
        )
        assert list(qs) == [team_member]

    def test_filter_by_user(self, team_member: TeamMember) -> None:
        """Test filter_by_user."""
        assert TeamMember.objects.filter_by_user(team_member.user).count() == 1

    # TODO make me a selector
    def test_filter_by_user_with_unrelated_team_member(
        self,
        workspace: Workspace,
        team_member: TeamMember,
        unrelated_user: User,
    ) -> None:
        """Test filtering when an unrelated team member exists."""
        assert TeamMember.objects.filter_by_user(team_member.user).count() == 1
        assert (
            TeamMember.objects.filter_by_user(
                unrelated_user,
            ).count()
            == 0
        )
        workspace_add_user(
            workspace=workspace,
            user=unrelated_user,
            role=TeamMemberRoles.OBSERVER,
        )
        assert TeamMember.objects.filter_by_user(unrelated_user).count() == 2


@pytest.mark.django_db
class TestTeamMember:
    """Test TeamMember."""

    def test_factory(self, team_member: TeamMember) -> None:
        """Test that the default rule is observer."""
        assert team_member.role == TeamMemberRoles.OWNER

    def test_assign_role(self, team_member: TeamMember) -> None:
        """Test assign_role."""
        team_member.assign_role(TeamMemberRoles.OWNER)
        team_member.refresh_from_db()
        assert team_member.role == TeamMemberRoles.OWNER
