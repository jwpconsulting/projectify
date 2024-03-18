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
"""Test team member views."""
from django.urls import (
    reverse,
)

import pytest
from rest_framework import status
from rest_framework.test import (
    APIClient,
)

from pytest_types import DjangoAssertNumQueries

from ...models.team_member import (
    TeamMember,
)


@pytest.mark.django_db
class TestTeamMemberReadUpdateDelete:
    """Test team member RUD."""

    @pytest.fixture
    def resource_url(self, team_member: TeamMember) -> str:
        """Return the resource url to the fixture team member."""
        return reverse(
            "workspace:team-members:read-update-delete",
            args=(str(team_member.uuid),),
        )

    def test_read(
        self,
        rest_user_client: APIClient,
        resource_url: str,
        team_member: TeamMember,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Test reading a user."""
        with django_assert_num_queries(2):
            response = rest_user_client.get(resource_url)
            assert response.status_code == status.HTTP_200_OK, response.data
        assert response.data["job_title"] == team_member.job_title

    def test_update(
        self,
        rest_user_client: APIClient,
        resource_url: str,
        team_member: TeamMember,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Test reading a user."""
        with django_assert_num_queries(6):
            response = rest_user_client.put(
                resource_url,
                data={
                    "job_title": "World famous plumber from Brooklyn",
                    "role": "OBSERVER",
                },
            )
            assert response.status_code == status.HTTP_200_OK, response.data
        assert response.data == {
            "job_title": "World famous plumber from Brooklyn",
            "role": "OBSERVER",
        }

    def test_delete_self(
        self,
        rest_user_client: APIClient,
        resource_url: str,
    ) -> None:
        """Test that deleting oneself does not work."""
        response = rest_user_client.delete(resource_url)
        assert response.status_code == 400, response.data
        assert response.data["team_member"] == "Can't delete own team member"

    def test_delete_other(
        self,
        rest_user_client: APIClient,
        team_member: TeamMember,
        other_team_member: TeamMember,
    ) -> None:
        """Test deleting another user."""
        resource_url = reverse(
            "workspace:team-members:read-update-delete",
            args=(str(other_team_member.uuid),),
        )
        response = rest_user_client.delete(resource_url)
        assert response.status_code == 204, response.data
        # The second time, the user is now gone
        response = rest_user_client.delete(resource_url)
        assert response.status_code == 404, response.data
