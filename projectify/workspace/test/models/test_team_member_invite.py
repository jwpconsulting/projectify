# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023-2024 JWP Consulting GK
"""Test TeamMemberInvite model."""

import pytest

from ...models import TeamMemberInvite


@pytest.mark.django_db
class TestTeamMemberInvite:
    """Test team member invite."""

    def test_factory(self, team_member_invite: TeamMemberInvite) -> None:
        """Test factory."""
        assert team_member_invite
