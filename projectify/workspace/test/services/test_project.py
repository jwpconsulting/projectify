# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023 JWP Consulting GK
"""Test project services."""

import pytest

from projectify.user.models import User

from ...models import Project, TeamMember, Workspace
from ...services.project import project_archive, project_create

pytestmark = pytest.mark.django_db


def test_project_create(
    workspace: Workspace, user: User, team_member: TeamMember
) -> None:
    """Test adding a project."""
    assert workspace.project_set.count() == 0
    board = project_create(
        workspace=workspace,
        title="foo",
        description="bar",
        who=user,
    )
    assert workspace.project_set.count() == 1
    board2 = project_create(
        workspace=workspace,
        title="foo",
        description="bar",
        who=user,
    )
    assert workspace.project_set.count() == 2
    # Projects are ordered by most recently created
    assert list(workspace.project_set.all()) == [
        board2,
        board,
    ]


def test_archive(project: Project, team_member: TeamMember) -> None:
    """Test archive method."""
    assert project.archived is None
    project_archive(project=project, archived=True, who=team_member.user)
    assert project.archived is not None


def test_unarchive(project: Project, team_member: TeamMember) -> None:
    """Test unarchive method."""
    assert project.archived is None
    project_archive(project=project, archived=True, who=team_member.user)
    assert project.archived is not None
    project_archive(
        project=project,
        archived=False,
        who=team_member.user,
    )
    assert project.archived is None
