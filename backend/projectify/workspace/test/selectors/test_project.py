# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023 JWP Consulting GK
"""Test project selectors."""

import pytest

from projectify.workspace.services.project import (
    project_archive,
)

from ...models.project import Project
from ...models.team_member import TeamMember
from ...selectors.project import (
    project_find_by_project_uuid,
    project_find_by_workspace_uuid,
)

# So apparently this is also possible:
pytestmark = pytest.mark.django_db
# See https://docs.pytest.org/en/stable/example/markers.html#scoped-marking


def test_project_find_by_workspace_uuid(
    project: Project,
    team_member: TeamMember,
    unrelated_team_member: TeamMember,
) -> None:
    """Test project_find_by_workspace_uuid."""
    qs = project_find_by_workspace_uuid(
        who=team_member.user,
        workspace_uuid=team_member.workspace.uuid,
    )
    assert qs.get() == project

    # Unrelated user can not access
    qs = project_find_by_workspace_uuid(
        who=unrelated_team_member.user,
        workspace_uuid=team_member.workspace.uuid,
    )
    assert qs.count() == 0

    # Filter by ONLY archived, and we will get nothing
    qs = project_find_by_workspace_uuid(
        who=team_member.user,
        workspace_uuid=team_member.workspace.uuid,
        archived=True,
    )
    assert qs.count() == 0


def test_project_find_by_project_uuid(
    project: Project,
    team_member: TeamMember,
    unrelated_team_member: TeamMember,
    unrelated_project: Project,
) -> None:
    """Test finding project for a user by UUID."""
    # Normal case, user finds their project
    assert project_find_by_project_uuid(
        project_uuid=project.uuid,
        who=team_member.user,
    )
    # Unrelated user finds their board
    assert project_find_by_project_uuid(
        project_uuid=unrelated_project.uuid,
        who=unrelated_team_member.user,
    )
    # Unrelated team member does not have access
    assert (
        project_find_by_project_uuid(
            project_uuid=project.uuid,
            who=unrelated_team_member.user,
        )
        is None
    )
    # And our user can not see unrelated user's board
    assert (
        project_find_by_project_uuid(
            project_uuid=unrelated_project.uuid,
            who=team_member.user,
        )
        is None
    )

    # Archiving hides it unless passing extra flag
    project_archive(
        who=team_member.user,
        project=project,
        archived=True,
    )
    assert (
        project_find_by_project_uuid(
            project_uuid=project.uuid,
            who=team_member.user,
        )
        is None
    )
    # Passing archived will make it show up again
    assert project_find_by_project_uuid(
        project_uuid=project.uuid,
        who=team_member.user,
        archived=True,
    )
