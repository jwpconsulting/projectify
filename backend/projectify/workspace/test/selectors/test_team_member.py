# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023 JWP Consulting GK
"""Test team member selectors."""

import pytest

from projectify.user.models import User
from projectify.workspace.models.team_member import TeamMember
from projectify.workspace.models.workspace import Workspace
from projectify.workspace.selectors.team_member import (
    team_member_find_for_workspace,
)


@pytest.mark.django_db
def test_team_member_find_for_workspace(
    workspace: Workspace,
    user: User,
    team_member: TeamMember,
) -> None:
    """Test get_by_workspace_and_user."""
    assert (
        team_member_find_for_workspace(
            workspace=workspace,
            user=user,
        )
        == team_member
    )
