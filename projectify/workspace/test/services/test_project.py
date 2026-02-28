# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023 JWP Consulting GK
"""Test project services."""

import pytest

from ...models import Project, TeamMember
from ...services.project import project_archive


@pytest.mark.django_db
def test_archive(project: Project, team_member: TeamMember) -> None:
    """Test archive method."""
    assert project.archived is None
    project_archive(project=project, archived=True, who=team_member.user)
    assert project.archived is not None


@pytest.mark.django_db
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
