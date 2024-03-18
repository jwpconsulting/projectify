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
"""Test label views."""
from django.urls import reverse

import pytest
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.test import APIClient

from projectify.workspace.models.label import Label
from projectify.workspace.models.team_member import TeamMember
from projectify.workspace.models.workspace import Workspace
from pytest_types import DjangoAssertNumQueries


@pytest.mark.django_db
class TestLabelCreate:
    """Test label creation."""

    @pytest.fixture
    def resource_url(self) -> str:
        """Return URL to this view."""
        return reverse("workspace:labels:create")

    def test_authenticated_user(
        self,
        rest_user_client: APIClient,
        resource_url: str,
        django_assert_num_queries: DjangoAssertNumQueries,
        workspace: Workspace,
        # Make sure we have a user
        team_member: TeamMember,
    ) -> None:
        """Test as an authenticated user."""
        # Gone up from 6 to 9 after introducing full_clean
        # Now 8
        with django_assert_num_queries(7):
            response = rest_user_client.post(
                resource_url,
                data={
                    "color": 0,
                    "name": "Bug",
                    "workspace_uuid": str(workspace.uuid),
                },
            )
        assert response.status_code == 201, response.data
        assert response.data["name"] == "Bug"

    def test_duplicate_create(
        self,
        rest_user_client: APIClient,
        resource_url: str,
        django_assert_num_queries: DjangoAssertNumQueries,
        workspace: Workspace,
        # Make sure we have a user
        team_member: TeamMember,
    ) -> None:
        """Assert we get a nice 400 on duplicate labels."""
        # Gone up from 6 to 9 after introducing full_clean
        payload = {
            "color": 0,
            "name": "Bug",
            "workspace_uuid": str(workspace.uuid),
        }
        response = rest_user_client.post(
            resource_url,
            data=payload,
        )
        assert response.status_code == 201, response.data
        response = rest_user_client.post(
            resource_url,
            data=payload,
        )
        assert response.status_code == 400, response.data


@pytest.mark.django_db
class TestLabelUpdateDelete:
    """Test updating and deleting labels."""

    @pytest.fixture
    def resource_url(self, label: Label) -> str:
        """Return URL to this view."""
        return reverse(
            "workspace:labels:update-delete", args=(str(label.uuid),)
        )

    def test_updating(
        self,
        rest_user_client: APIClient,
        resource_url: str,
        django_assert_num_queries: DjangoAssertNumQueries,
        team_member: TeamMember,
        label: Label,
    ) -> None:
        """Test updating a label."""
        # Gone up from 7 to 10 after introducing full_clean
        # now 9
        # now 8 yay
        with django_assert_num_queries(7):
            response = rest_user_client.put(
                resource_url,
                data={
                    "color": 2,
                    "name": "New name for a label",
                },
            )
            assert response.status_code == 200, response.data
        label.refresh_from_db()
        assert label.name == "New name for a label"
        assert label.color == 2
        assert response.data["name"] == "New name for a label"

    def test_deleting(
        self,
        rest_user_client: APIClient,
        resource_url: str,
        django_assert_num_queries: DjangoAssertNumQueries,
        team_member: TeamMember,
        label: Label,
    ) -> None:
        """Test deleting a label."""
        with django_assert_num_queries(5):
            response = rest_user_client.delete(resource_url)
            assert response.status_code == HTTP_204_NO_CONTENT, response.data
        assert Label.objects.count() == 0
