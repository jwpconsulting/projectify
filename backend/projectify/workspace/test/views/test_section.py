# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023 JWP Consulting GK
"""Test section CRUD views."""

from uuid import uuid4

from django.contrib.auth.models import AbstractBaseUser
from django.http import HttpResponseRedirect
from django.test import Client
from django.urls import reverse

import pytest
from rest_framework import status
from rest_framework.test import APIClient

from projectify.workspace.models import Project, Section, TaskLabel
from projectify.workspace.models.task import Task
from projectify.workspace.models.team_member import TeamMember
from projectify.workspace.models.workspace import Workspace
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
        self,
        user_client: Client,
        team_member: TeamMember,
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
        with django_assert_num_queries(5):
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

        with django_assert_num_queries(7):
            response = user_client.post(
                resource_url,
                {"action": "save", "title": new_title},
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
        response = user_client.post(
            resource_url,
            {"action": "save"},
        )
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

        with django_assert_num_queries(8):
            response = user_client.post(
                resource_url,
                {"action": "move_up"},
            )
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
        Section.objects.create(
            project=section.project,
            title="Other section",
        )
        original_order = section._order

        # TODO optimize
        with django_assert_num_queries(15):
            response = user_client.post(
                resource_url,
                {"action": "move_down"},
            )
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


class TestSectionMinimizeView:
    """Test section minimize view."""

    @pytest.mark.parametrize(
        "initial_state,form_value,expected_final_state",
        [
            (False, "true", True),  # minimize section
            (True, "false", False),  # expand section
        ],
    )
    def test_section_minimize_toggle(
        self,
        user_client: Client,
        team_member: TeamMember,
        section: Section,
        initial_state: bool,
        form_value: str,
        expected_final_state: bool,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Test minimizing and expanding a section."""
        if initial_state:
            section.minimized_by.add(team_member.user)

        assert (
            section.minimized_by.filter(pk=team_member.user.pk).exists()
            == initial_state
        )

        with django_assert_num_queries(7):
            response = user_client.post(
                reverse("dashboard:sections:minimize", args=[section.uuid]),
                {"minimized": form_value},
            )

        assert response.status_code == 302
        assert isinstance(response, HttpResponseRedirect)

        section.refresh_from_db()
        assert (
            section.minimized_by.filter(pk=team_member.user.pk).exists()
            == expected_final_state
        )

    def test_minimize_section_different_workspace(
        self, user_client: Client, unrelated_section: Section
    ) -> None:
        """Test minimize view with section from different workspace."""
        response = user_client.post(
            reverse(
                "dashboard:sections:minimize", args=[unrelated_section.uuid]
            ),
            {"minimized": "true"},
        )
        assert response.status_code == 404


# Create
class TestSectionCreate:
    """Test section creation."""

    @pytest.fixture
    def resource_url(self) -> str:
        """Return URL to this view."""
        return reverse("workspace:sections:create")

    def test_authenticated(
        self,
        user: AbstractBaseUser,
        rest_user_client: APIClient,
        resource_url: str,
        django_assert_num_queries: DjangoAssertNumQueries,
        project: Project,
        # Make sure that we are part of that workspace
        team_member: TeamMember,
    ) -> None:
        """Assert that we can create a new project."""
        assert Section.objects.count() == 0
        with django_assert_num_queries(7):
            response = rest_user_client.post(
                resource_url,
                {
                    "title": "New section, who dis??",
                    "project_uuid": str(project.uuid),
                },
            )
        assert response.status_code == 201
        assert Section.objects.count() == 1
        section = Section.objects.get()
        assert section.title == "New section, who dis??"


# Read + Update + Delete
class TestSectionReadUpdateDelete:
    """Test SectionReadUpdateDelete view."""

    @pytest.fixture
    def resource_url(self, section: Section) -> str:
        """Return URL to this view."""
        return reverse(
            "workspace:sections:read-update-delete",
            args=(section.uuid,),
        )

    def test_get(
        self,
        rest_user_client: APIClient,
        resource_url: str,
        user: AbstractBaseUser,
        workspace: Workspace,
        team_member: TeamMember,
        task: Task,
        other_task: Task,
        task_label: TaskLabel,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Assert we can post to this view this while being logged in."""
        # Make sure task -> team_member -> user is resolved
        task.assignee = team_member
        task.save()
        with django_assert_num_queries(7):
            response = rest_user_client.get(resource_url)
            assert response.status_code == 200, response.content

    def test_update(
        self,
        rest_user_client: APIClient,
        resource_url: str,
        user: AbstractBaseUser,
        team_member: TeamMember,
        django_assert_num_queries: DjangoAssertNumQueries,
        section: Section,
    ) -> None:
        """Test updating a section."""
        with django_assert_num_queries(5):
            response = rest_user_client.put(
                resource_url,
                data={
                    "title": "New title",
                    "description": "New description",
                },
            )
            assert response.status_code == status.HTTP_200_OK, response.data
        assert response.data == {
            "title": "New title",
            "description": "New description",
        }
        section.refresh_from_db()
        assert section.title == "New title"
        assert section.description == "New description"

    def test_delete(
        self,
        rest_user_client: APIClient,
        resource_url: str,
        team_member: TeamMember,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Test deleting."""
        with django_assert_num_queries(9):
            response = rest_user_client.delete(resource_url)
            assert (
                response.status_code == status.HTTP_204_NO_CONTENT
            ), response.data
        assert Section.objects.count() == 0


# RPC
class TestSectionMove:
    """Test moving a section."""

    @pytest.fixture
    def resource_url(self, section: Section) -> str:
        """Return URL to this view."""
        return reverse(
            "workspace:sections:move",
            args=(str(section.uuid),),
        )

    def test_authenticated_user(
        self,
        rest_user_client: APIClient,
        resource_url: str,
        django_assert_num_queries: DjangoAssertNumQueries,
        section: Section,
        team_member: TeamMember,
    ) -> None:
        """Test as an authenticated user."""
        other_section = Section(
            project=section.project,
            title="test",
        )
        other_section.save()
        assert section._order == 0
        assert other_section._order == 1
        # XXX that's still a whole lot of queries
        # 50% XXX Better now
        with django_assert_num_queries(11):
            response = rest_user_client.post(
                resource_url,
                data={
                    "order": 1,
                },
            )

        assert response.status_code == status.HTTP_200_OK, response.data
        section.refresh_from_db()
        other_section.refresh_from_db()
        assert other_section._order == 0
        assert section._order == 1
