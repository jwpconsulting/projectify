# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2024 JWP Consulting GK
"""Test workspace model selectors."""

import pytest

from ...models.team_member import TeamMember
from ...selectors.workspace import (
    workspace_find_by_workspace_uuid,
    workspace_find_for_user,
)
from ...services.workspace import workspace_delete

pytestmark = pytest.mark.django_db


def test_workspace_find_for_user(
    team_member: TeamMember, unrelated_team_member: TeamMember
) -> None:
    """Test workspace_find_for_user."""
    a = team_member
    b = unrelated_team_member
    assert workspace_find_for_user(who=a.user).count() == 1
    assert workspace_find_for_user(who=b.user).count() == 1
    workspace_delete(who=a.user, workspace=a.workspace)
    assert workspace_find_for_user(who=a.user).count() == 0
    assert workspace_find_for_user(who=b.user).count() == 1
    workspace_delete(who=b.user, workspace=b.workspace)
    assert workspace_find_for_user(who=a.user).count() == 0
    assert workspace_find_for_user(who=b.user).count() == 0


def test_workspace_find_by_workspace_uuid(
    team_member: TeamMember, unrelated_team_member: TeamMember
) -> None:
    """Test workspace_find_by_workspace_uuid."""
    a = team_member
    b = unrelated_team_member
    # A can find A's workspace
    assert workspace_find_by_workspace_uuid(
        who=a.user, workspace_uuid=a.workspace.uuid
    )
    # B can find B's workspace
    assert workspace_find_by_workspace_uuid(
        who=b.user, workspace_uuid=b.workspace.uuid
    )
    # A can't find B's workspace
    assert (
        workspace_find_by_workspace_uuid(
            who=a.user, workspace_uuid=b.workspace.uuid
        )
        is None
    )
    # B can't find A's workspace
    assert (
        workspace_find_by_workspace_uuid(
            who=b.user, workspace_uuid=a.workspace.uuid
        )
        is None
    )
