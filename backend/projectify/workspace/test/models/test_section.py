# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023 JWP Consulting GK
"""Section model tests."""

import pytest

from ... import models


@pytest.mark.django_db
class TestSectionManager:
    """Test Section manager."""

    def test_filter_by_project_pks(
        self,
        project: models.Project,
        section: models.Section,
    ) -> None:
        """Test filter_by_project_pks."""
        objects = models.Section.objects
        qs = objects.filter_by_project_pks(
            [project.pk],
        )
        assert list(qs) == [section]

    def test_filter_for_user_and_uuid(
        self,
        section: models.Section,
        team_member: models.TeamMember,
        # TODO are these two fixtures needed?
        workspace: models.Workspace,
        other_team_member: models.TeamMember,
    ) -> None:
        """Test getting for user and uuid."""
        actual = models.Section.objects.filter_for_user_and_uuid(
            team_member.user,
            section.uuid,
        ).get()
        assert actual == section


@pytest.mark.django_db
class TestSection:
    """Test Section."""

    def test_factory(
        self,
        project: models.Project,
        section: models.Section,
    ) -> None:
        """Test section creation works."""
        assert section.project == project
