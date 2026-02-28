# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023 JWP Consulting GK
"""Test team member selectors."""

import pytest

from projectify.user.models import User

from ...models import Project, TeamMember, Workspace
from ...selectors.team_member import (
    team_member_find_for_workspace,
    team_member_last_project_for_user,
    team_member_last_workspace_for_user,
)
from ...services.team_member import (
    team_member_visit_project,
    team_member_visit_workspace,
)

pytestmark = pytest.mark.django_db


def test_team_member_find_for_workspace(
    workspace: Workspace,
    user: User,
    team_member: TeamMember,
) -> None:
    """Test get_by_workspace_and_user."""
    assert (
        team_member_find_for_workspace(workspace=workspace, user=user)
        == team_member
    )


def test_team_member_multiple_workspaces(
    team_member: TeamMember, workspace: Workspace, other_workspace: Workspace
) -> None:
    """Test that we receive the most recently visited workspace."""
    user = team_member.user
    # No last visited in the beginning
    assert team_member_last_workspace_for_user(user=user) is None
    team_member_visit_workspace(team_member=team_member)
    assert team_member_last_workspace_for_user(user=user) == workspace

    other_team_member = other_workspace.teammember_set.get()
    team_member_visit_workspace(team_member=other_team_member)
    assert team_member_last_workspace_for_user(user=user) == other_workspace

    team_member_visit_workspace(team_member=team_member)
    assert team_member_last_workspace_for_user(user=user) == workspace

    # This will not set a last visited project
    assert (
        team_member_last_project_for_user(
            user=team_member.user, workspace=team_member.workspace
        )
        is None
    )


def test_team_member_multiple_projects(
    team_member: TeamMember,
    workspace: Workspace,
    project: Project,
    other_project_same_workspace: Project,
) -> None:
    """
    Test that we get the most recently visited project in workspace A.

    Visiting project C in another workspace B should not affect the
    result for workspace A.
    """
    user = team_member.user
    assert (
        team_member_last_project_for_user(user=user, workspace=workspace)
        is None
    )

    team_member_visit_project(team_member=team_member, project=project)
    assert (
        team_member_last_project_for_user(user=user, workspace=workspace)
        == project
    )

    team_member_visit_project(
        team_member=team_member, project=other_project_same_workspace
    )
    assert (
        team_member_last_project_for_user(user=user, workspace=workspace)
        == other_project_same_workspace
    )

    team_member_visit_project(team_member=team_member, project=project)
    assert (
        team_member_last_project_for_user(user=user, workspace=workspace)
        == project
    )
    assert team_member_last_workspace_for_user(user=user) == workspace


def test_team_member_preferences_other_project(
    team_member: TeamMember, other_workspace: Workspace, project: Project
) -> None:
    """
    Test that preferences for different workspaces don't interfere.

    When I visit project A in workspace A, then my last visited project
    for workspace B shouldn't change.
    """
    user = team_member.user
    team_member_visit_project(team_member=team_member, project=project)

    assert (
        team_member_last_project_for_user(user=user, workspace=other_workspace)
        is None
    )
