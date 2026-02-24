# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023 JWP Consulting GK
"""Test section CRUD views."""

from uuid import uuid4

from django.http import HttpResponseRedirect
from django.test import Client
from django.urls import reverse

import pytest

from projectify.workspace.models import Section
from projectify.workspace.models.team_member import TeamMember
from pytest_types import DjangoAssertNumQueries

pytestmark = pytest.mark.django_db


# HTML Views
class TestSectionDetail:
    """Test section detail view."""

    @pytest.fixture
    def resource_url(self, section: Section) -> str:
        """Return URL to this view."""
        return reverse("dashboard:sections:detail", args=(section.uuid,))

    def test_get_section_detail_redirects_to_project(
        self,
        user_client: Client,
        resource_url: str,
        section: Section,
        team_member: TeamMember,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Test that section detail redirects to project with section anchor."""
        with django_assert_num_queries(4):
            response = user_client.get(resource_url)
            assert response.status_code == 302

        assert isinstance(response, HttpResponseRedirect)
        assert str(section.project.uuid) in response.url
        assert str(section.uuid) in response.url

    def test_section_not_found(
        self, user_client: Client, team_member: TeamMember
    ) -> None:
        """Test accessing non-existent section returns 404."""
        url = reverse("dashboard:sections:detail", args=(uuid4(),))
        response = user_client.get(url)
        assert response.status_code == 404


class TestSectionUpdateView:
    """Test section update view."""

    @pytest.fixture
    def resource_url(self, section: Section) -> str:
        """Return URL to this view."""
        return reverse("dashboard:sections:update", args=(section.uuid,))

    def test_get_section_update_form(
        self,
        user_client: Client,
        resource_url: str,
        section: Section,
        team_member: TeamMember,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Test getting the section update form."""
        with django_assert_num_queries(7):
            response = user_client.get(resource_url)
            assert response.status_code == 200
        assert "Update Section" in response.content.decode()
        assert section.title in response.content.decode()

    def test_post_save_section(
        self,
        user_client: Client,
        resource_url: str,
        section: Section,
        team_member: TeamMember,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Test saving section updates."""
        new_title = "Updated Section Title"

        with django_assert_num_queries(9):
            response = user_client.post(
                resource_url, {"action": "save", "title": new_title}
            )
            assert response.status_code == 302

        section.refresh_from_db()
        assert section.title == new_title

    def test_post_save_section_empty_title(
        self,
        user_client: Client,
        resource_url: str,
        team_member: TeamMember,
    ) -> None:
        """Test saving section with empty title shows error."""
        response = user_client.post(resource_url, {"action": "save"})
        assert response.status_code == 400

    def test_post_move_up(
        self,
        user_client: Client,
        resource_url: str,
        section: Section,
        team_member: TeamMember,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Test moving section up."""
        Section.objects.create(project=section.project, title="Other section")

        original_order = section._order

        with django_assert_num_queries(10):
            response = user_client.post(resource_url, {"action": "move_up"})
            assert response.status_code == 302

        # Won't change
        section.refresh_from_db()
        assert section._order == original_order

    def test_post_move_down(
        self,
        user_client: Client,
        resource_url: str,
        section: Section,
        team_member: TeamMember,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Test moving section down."""
        Section.objects.create(project=section.project, title="Other section")
        original_order = section._order

        # TODO optimize
        with django_assert_num_queries(17):
            response = user_client.post(resource_url, {"action": "move_down"})
            assert response.status_code == 302

        section.refresh_from_db()
        assert section._order == original_order + 1

    def test_section_not_found(
        self,
        user_client: Client,
        team_member: TeamMember,
    ) -> None:
        """Test accessing non-existent section returns 404."""
        url = reverse("dashboard:sections:update", args=(uuid4(),))
        response = user_client.get(url)
        assert response.status_code == 404
