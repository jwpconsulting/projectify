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
"""Project model tests."""
import pytest

from ...models.project import Project
from ...models.workspace import Workspace
from ...models.team_member import TeamMember
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
