# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023 JWP Consulting GK
"""Project model tests."""

import pytest

from ...models.project import Project
from ...models.team_member import TeamMember
from ...models.workspace import Workspace
from ...services.section import section_create


@pytest.mark.django_db
class TestProject:
    """Test Project."""

    def test_factory(
        self,
        workspace: Workspace,
        project: Project,
    ) -> None:
        """Test project creation works."""
        assert project.workspace == workspace

    def test_add_section(
        self,
        project: Project,
        team_member: TeamMember,
    ) -> None:
        """Test section creation."""
        assert project.section_set.count() == 0
        section = section_create(
            who=team_member.user,
            project=project,
            title="hello",
            description="world",
        )
        assert project.section_set.count() == 1
        section2 = section_create(
            who=team_member.user,
            project=project,
            title="hello",
            description="world",
        )
        assert project.section_set.count() == 2
        assert list(project.section_set.all()) == [
            section,
            section2,
        ]
