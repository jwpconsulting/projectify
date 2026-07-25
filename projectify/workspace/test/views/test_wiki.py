# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2026 JWP Consulting GK
"""Test wiki views."""

from uuid import UUID

from django.test.client import Client
from django.urls import reverse

import pytest

from pytest_types import DjangoAssertNumQueries

from ...models import TeamMember, WikiPage, Workspace

pytestmark = pytest.mark.django_db


class TestWikiIndexView:
    """Test wiki index view."""

    @pytest.fixture
    def resource_url(self, team_member: TeamMember) -> str:
        """Return URL to this view."""
        w = team_member.workspace.uuid
        return reverse("dashboard:wiki:index", args=(w,))

    def test_get(
        self,
        user_client: Client,
        resource_url: str,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Test GETting the wiki index page."""
        with django_assert_num_queries(13):
            assert user_client.get(resource_url).status_code == 200

    def test_get_unrelated_user(
        self, unrelated_user_client: Client, resource_url: str
    ) -> None:
        """Test that unrelated users can't access the wiki index."""
        assert unrelated_user_client.get(resource_url).status_code == 404

    def test_workspace_not_found(
        self, user_client: Client, null_uuid: UUID
    ) -> None:
        """Test accessing wiki index for non-existent workspace."""
        url = reverse("dashboard:wiki:index", args=(null_uuid,))
        assert user_client.get(url).status_code == 404


class TestWikiRecentChangesView:
    """Test wiki recent changes view."""

    @pytest.fixture
    def resource_url(self, team_member: TeamMember) -> str:
        """Return URL to this view."""
        w = team_member.workspace.uuid
        return reverse("dashboard:wiki:recent-changes", args=(w,))

    def test_get(
        self,
        user_client: Client,
        resource_url: str,
        wiki_page: WikiPage,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Test GETting the recent changes page."""
        with django_assert_num_queries(9):
            response = user_client.get(resource_url)
            assert response.status_code == 200
        assert wiki_page.title in response.content.decode()

    def test_get_no_pages(
        self, user_client: Client, resource_url: str
    ) -> None:
        """Test recent changes page with no wiki pages."""
        response = user_client.get(resource_url)
        assert response.status_code == 200
        assert b"No wiki pages found." in response.content

    def test_get_unrelated_user(
        self, unrelated_user_client: Client, resource_url: str
    ) -> None:
        """Test that unrelated users can't access recent changes."""
        assert unrelated_user_client.get(resource_url).status_code == 404

    def test_workspace_not_found(
        self, user_client: Client, null_uuid: UUID
    ) -> None:
        """Test accessing recent changes for non-existent workspace."""
        url = reverse("dashboard:wiki:recent-changes", args=(null_uuid,))
        assert user_client.get(url).status_code == 404


class TestWikiPageView:
    """Test wiki page view."""

    @pytest.fixture
    def resource_url(
        self, team_member: TeamMember, wiki_page: WikiPage
    ) -> str:
        """Return URL to this view."""
        w = team_member.workspace.uuid
        return reverse("dashboard:wiki:view", args=(w, wiki_page.title))

    def test_get_existing_page(
        self,
        user_client: Client,
        resource_url: str,
        wiki_page: WikiPage,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Test GETting an existing wiki page."""
        with django_assert_num_queries(7):
            response = user_client.get(resource_url)
            assert response.status_code == 200
        assert wiki_page.title in response.content.decode()

    def test_get_new_page(
        self, user_client: Client, workspace: Workspace
    ) -> None:
        """Test GETting a non-existent wiki page redirects to edit view."""
        url = reverse("dashboard:wiki:view", args=(workspace.uuid, "b"))
        response = user_client.get(url)
        assert response.status_code == 302
        assert response["Location"] == reverse(
            "dashboard:wiki:edit", args=(workspace.uuid, "b")
        )

    def test_get_unrelated_user(
        self, unrelated_user_client: Client, resource_url: str
    ) -> None:
        """Test that unrelated users can't access wiki pages."""
        assert unrelated_user_client.get(resource_url).status_code == 404

    def test_workspace_not_found(
        self, user_client: Client, wiki_page: WikiPage, null_uuid: UUID
    ) -> None:
        """Test accessing a wiki page for a non-existent workspace."""
        url = reverse("dashboard:wiki:view", args=(null_uuid, wiki_page.title))
        assert user_client.get(url).status_code == 404


class TestWikiPageEditView:
    """Test wiki page edit view."""

    @pytest.fixture
    def resource_url(
        self, team_member: TeamMember, wiki_page: WikiPage
    ) -> str:
        """Return URL to this view."""
        ws = team_member.workspace.uuid
        return reverse("dashboard:wiki:edit", args=(ws, wiki_page.title))

    def test_get(
        self,
        user_client: Client,
        resource_url: str,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Test GETting the wiki page edit form."""
        with django_assert_num_queries(7):
            assert user_client.get(resource_url).status_code == 200

    def test_post_success(
        self, user_client: Client, resource_url: str, wiki_page: WikiPage
    ) -> None:
        """Test successfully updating a wiki page."""
        d = {"content": "<p>Updated content</p>"}
        assert user_client.post(resource_url, d).status_code == 302
        wiki_page.refresh_from_db()
        assert "<p>Updated content</p>" in wiki_page.content

    def test_get_unrelated_user(
        self, unrelated_user_client: Client, resource_url: str
    ) -> None:
        """Test that unrelated users can't edit wiki pages."""
        assert unrelated_user_client.get(resource_url).status_code == 404

    def test_get_new_page(
        self, user_client: Client, workspace: Workspace
    ) -> None:
        """Test GETting the edit view for a non-existent page shows create form."""
        url = reverse("dashboard:wiki:edit", args=(workspace.uuid, "n"))
        assert user_client.get(url).status_code == 200

    def test_post_create_new_page(
        self, user_client: Client, workspace: Workspace
    ) -> None:
        """Test POSTing to the edit view for a non-existent page creates it."""
        initial_count = WikiPage.objects.count()
        url = reverse("dashboard:wiki:edit", args=(workspace.uuid, "n"))
        d = {"content": "<p>Hello world</p>"}
        assert user_client.post(url, d).status_code == 302
        assert WikiPage.objects.count() == initial_count + 1
