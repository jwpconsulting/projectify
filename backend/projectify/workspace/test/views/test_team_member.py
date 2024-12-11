# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023 JWP Consulting GK
"""Test team member views."""

from unittest.mock import ANY

from django.urls import reverse

import pytest
from rest_framework import status
from rest_framework.test import APIClient

from pytest_types import DjangoAssertNumQueries

from ...models.team_member import TeamMember


@pytest.mark.django_db
class TestTeamMemberReadUpdateDelete:
    """Test team member RUD."""

    @pytest.fixture
    def resource_url(self, other_team_member: TeamMember) -> str:
        """Return the resource url to the fixture team member."""
        return reverse(
            "workspace:team-members:read-update-delete",
            args=(str(other_team_member.uuid),),
        )

    def test_read(
        self,
        rest_user_client: APIClient,
        resource_url: str,
        other_team_member: TeamMember,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Test reading a user."""
        with django_assert_num_queries(1):
            response = rest_user_client.get(resource_url)
            assert response.status_code == status.HTTP_200_OK, response.data
        assert response.data == {
            "uuid": str(other_team_member.uuid),
            "job_title": ANY,
            "role": ANY,
            "user": ANY,
        }

    def test_read_unrelated(
        self,
        rest_user_client: APIClient,
        unrelated_team_member: TeamMember,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Test reading a team member from another workspace."""
        resource_url = reverse(
            "workspace:team-members:read-update-delete",
            args=(str(unrelated_team_member.uuid),),
        )
        response = rest_user_client.get(resource_url)
        assert response.status_code == status.HTTP_404_NOT_FOUND, response.data

    def test_update(
        self,
        rest_user_client: APIClient,
        resource_url: str,
        team_member: TeamMember,
        other_team_member: TeamMember,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Test reading a user."""
        del team_member
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
            "uuid": ANY,
            "job_title": "World famous plumber from Brooklyn",
            "role": "OBSERVER",
            "user": {
                "email": other_team_member.user.email,
                "preferred_name": other_team_member.user.preferred_name,
                "profile_picture": other_team_member.user.profile_picture,
            },
        }

    def test_delete_self(
        self,
        rest_user_client: APIClient,
        team_member: TeamMember,
    ) -> None:
        """Test that deleting oneself does not work."""
        resource_url = reverse(
            "workspace:team-members:read-update-delete",
            args=(str(team_member.uuid),),
        )
        response = rest_user_client.delete(resource_url)
        assert response.status_code == 400, response.data
        assert response.data == {
            "status": "invalid",
            "code": 400,
            "details": {"team_member": "Can't delete own team member"},
            "general": None,
        }

    def test_delete_other(
        self,
        rest_user_client: APIClient,
        team_member: TeamMember,
        resource_url: str,
    ) -> None:
        """Test deleting another user."""
        del team_member
        response = rest_user_client.delete(resource_url)
        assert response.status_code == 204, response.data
        # The second time, the user is now gone
        response = rest_user_client.delete(resource_url)
        assert response.status_code == 404, response.data
