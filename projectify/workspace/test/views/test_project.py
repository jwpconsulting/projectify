# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023 JWP Consulting GK
"""Test project CRUD views."""

from datetime import datetime
from uuid import UUID

from django.test.client import Client
from django.urls import reverse

import pytest

from pytest_types import DjangoAssertNumQueries

from ...models import Project, Task, TeamMember, Workspace

pytestmark = pytest.mark.django_db


class TestProjectDetailView:
    """Test html project detail view."""

    @pytest.fixture
    def resource_url(self, project: Project) -> str:
        """Return URL to this view."""
        return reverse("dashboard:projects:detail", args=(project.uuid,))

    def test_get_project_detail(
        self,
        user_client: Client,
        resource_url: str,
        project: Project,
        team_member: TeamMember,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Test GETting the project detail page."""
        with django_assert_num_queries(15):
            response = user_client.get(resource_url)
            assert response.status_code == 200
        assert project.title in response.content.decode()
        assert project.workspace.title in response.content.decode()

    def test_project_not_found(
        self,
        user_client: Client,
        team_member: TeamMember,
        django_assert_num_queries: DjangoAssertNumQueries,
        null_uuid: UUID,
    ) -> None:
        """Ensure that accessing a non-existent project returns 404."""
        url = reverse("dashboard:projects:detail", args=(null_uuid,))
        with django_assert_num_queries(3):
            response = user_client.get(url)
            assert response.status_code == 404

    def test_archived_project_not_found(
        self,
        user_client: Client,
        archived_project: Project,
        team_member: TeamMember,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Ensure that the client can't access archived projects."""
        url = reverse(
            "dashboard:projects:detail", args=(archived_project.uuid,)
        )
        with django_assert_num_queries(3):
            response = user_client.get(url)
            assert response.status_code == 404


class TestProjectDetailViewActions:
    """Test project detail view actions."""

    @pytest.fixture
    def resource_url(self, project: Project) -> str:
        """Return URL to this view."""
        return reverse("dashboard:projects:detail", args=(project.uuid,))

    def test_quick_add_task_success(
        self, user_client: Client, resource_url: str, team_member: TeamMember
    ) -> None:
        """Test successfully creating a task via quick add."""
        initial_count = Task.objects.count()
        data = {"action": "quick_add_task", "title": "<h1>title"}
        assert user_client.post(resource_url, data).status_code == 200
        assert Task.objects.count() == initial_count + 1
        task = Task.objects.latest("modified")
        assert task.title == "<h1>title"

        # Test form validation, missing title
        data = {"action": "quick_add_task"}
        assert user_client.post(resource_url, data).status_code == 400
        assert Task.objects.count() == initial_count + 1

    def test_mark_task_done(
        self,
        user_client: Client,
        resource_url: str,
        team_member: TeamMember,
        task: Task,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Test marking a task as done and then not done."""
        assert task.done is None
        t_id = str(task.uuid)
        data = {"action": "mark_task_done", "task_uuid": t_id, "done": "true"}
        # Gone up from 24 -> 27 due to permission checks in template
        # Gone up from 27 -> 29 because of workspace save()
        # check
        # Gone down from 29 -> 28
        # Gone down from 28 -> 26
        # Gone down from 26 -> 22
        with django_assert_num_queries(22):
            response = user_client.post(resource_url, data)
            assert response.status_code == 200
        task.refresh_from_db()
        assert task.done is not None

        data = {"action": "mark_task_done", "task_uuid": t_id, "done": "false"}
        with django_assert_num_queries(22):
            response = user_client.post(resource_url, data)
            assert response.status_code == 200
        task.refresh_from_db()
        assert task.done is None

    def test_mark_task_done_form_validation(
        self, user_client: Client, resource_url: str, null_uuid: UUID
    ) -> None:
        """Test form validation for mark task done action."""
        d = {"action": "mark_task_done"}
        response = user_client.post(
            resource_url, {**d, "task_uuid": str(null_uuid), "done": "true"}
        )
        assert response.status_code == 400
        response = user_client.post(
            resource_url, {**d, "action": "mark_task_done", "done": "true"}
        )
        assert response.status_code == 400


class TestProjectCreateView:
    """Test html project create view."""

    @pytest.fixture
    def resource_url(self, workspace: Workspace) -> str:
        """Return URL to this view."""
        return reverse(
            "dashboard:workspaces:create-project", args=(workspace.uuid,)
        )

    def test_get(
        self,
        unrelated_user_client: Client,
        user_client: Client,
        resource_url: str,
        team_member: TeamMember,
    ) -> None:
        """Test getting this page."""
        assert unrelated_user_client.get(resource_url).status_code == 404
        assert user_client.get(resource_url).status_code == 200

    def test_create_project_success(
        self,
        user_client: Client,
        resource_url: str,
        team_member: TeamMember,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Test successfully creating a project."""
        initial_project_count = Project.objects.count()
        data = {"description": "<h1>New Test Project</h1>"}
        with django_assert_num_queries(8):
            response = user_client.post(resource_url, data)
            assert response.status_code == 302
        assert Project.objects.count() == initial_project_count + 1
        assert Project.objects.get().title == "New Test Project"

    def test_create_project_invalid_form(
        self, user_client: Client, resource_url: str, team_member: TeamMember
    ) -> None:
        """Test form validation with invalid data."""
        initial_project_count = Project.objects.count()
        assert user_client.post(resource_url, {}).status_code == 400
        assert Project.objects.count() == initial_project_count

    def test_workspace_not_found(
        self, user_client: Client, team_member: TeamMember, null_uuid: UUID
    ) -> None:
        """Test accessing project creation for non-existent workspace."""
        url = reverse("dashboard:workspaces:create-project", args=(null_uuid,))
        assert user_client.get(url).status_code == 404


class TestProjectUpdateView:
    """Test html project update view."""

    @pytest.fixture
    def resource_url(self, project: Project) -> str:
        """Return URL to this view."""
        return reverse("dashboard:projects:update", args=(project.uuid,))

    def test_get_project_update(
        self,
        unrelated_user_client: Client,
        user_client: Client,
        resource_url: str,
        project: Project,
        team_member: TeamMember,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Test GETting the project update page."""
        # Unauthorized access
        assert unrelated_user_client.get(resource_url).status_code == 404
        # Gone up   from 8 -> 9 due to permission checks in sidemenu
        with django_assert_num_queries(9):
            response = user_client.get(resource_url)
            assert response.status_code == 200
            assert project.title.encode() in response.content

    def test_post_success(
        self,
        user_client: Client,
        resource_url: str,
        project: Project,
        team_member: TeamMember,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Test successfully updating a project."""
        updated_title = "<h1>Updated Project Title</h1><p>foo bar</p>"

        data = {"description": updated_title}
        with django_assert_num_queries(9):
            response = user_client.post(resource_url, data)
            assert response.status_code == 302

        project.refresh_from_db()
        assert project.title == "Updated Project Title"
        assert (
            project.description
            == "<h1>Updated Project Title</h1><p>foo bar</p>"
        )

    def test_update_project_invalid_form(
        self,
        user_client: Client,
        resource_url: str,
        project: Project,
        team_member: TeamMember,
    ) -> None:
        """Test form validation with invalid data."""
        original_title = project.title
        response = user_client.post(resource_url, {"title_description": ""})
        assert response.status_code == 400
        project.refresh_from_db()
        assert project.title == original_title, "Shouldn't change"

    def test_project_not_found(
        self, user_client: Client, team_member: TeamMember, null_uuid: UUID
    ) -> None:
        """Ensure that updating a non-existent project returns 404."""
        url = reverse("dashboard:projects:update", args=(null_uuid,))
        response = user_client.get(url)
        assert response.status_code == 404

    def test_archived_project_not_found(
        self,
        user_client: Client,
        archived_project: Project,
        team_member: TeamMember,
    ) -> None:
        """Ensure that the client can't update archived projects."""
        url = reverse(
            "dashboard:projects:update", args=(archived_project.uuid,)
        )
        response = user_client.get(url)
        assert response.status_code == 404


class TestProjectArchiveView:
    """Test html project archive view."""

    @pytest.fixture
    def resource_url(self, project: Project) -> str:
        """Return URL to this view."""
        return reverse("dashboard:projects:archive", args=(project.uuid,))

    def test_post_archive_project(
        self,
        user_client: Client,
        resource_url: str,
        project: Project,
        team_member: TeamMember,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Test successfully archiving a project via HTMX."""
        assert not project.archived
        with django_assert_num_queries(8):
            response = user_client.post(resource_url)
            assert response.status_code == 200
        project.refresh_from_db()
        assert project.archived

    def test_project_not_found(
        self, user_client: Client, team_member: TeamMember, null_uuid: UUID
    ) -> None:
        """Test archiving a non-existent project returns 404."""
        url = reverse("dashboard:projects:archive", args=(null_uuid,))
        response = user_client.post(url)
        assert response.status_code == 404

    def test_already_archived_project_not_found(
        self,
        user_client: Client,
        archived_project: Project,
        team_member: TeamMember,
    ) -> None:
        """Test that already archived projects can't be archived again."""
        url = reverse(
            "dashboard:projects:archive", args=(archived_project.uuid,)
        )
        response = user_client.post(url)
        assert response.status_code == 404

    def test_unauthorized_project_access(
        self, user_client: Client, unrelated_project: Project
    ) -> None:
        """Test that users can't archive projects they don't have access to."""
        url = reverse(
            "dashboard:projects:archive", args=(unrelated_project.uuid,)
        )
        response = user_client.post(url)
        assert response.status_code == 404


class TestProjectRecoverView:
    """Test html project recover view."""

    @pytest.fixture
    def resource_url(self, archived_project: Project) -> str:
        """Return URL to this view."""
        return reverse(
            "dashboard:projects:recover", args=(archived_project.uuid,)
        )

    def test_post_recover_project(
        self,
        user_client: Client,
        resource_url: str,
        archived_project: Project,
        team_member: TeamMember,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Test successfully recovering an archived project via HTMX."""
        assert archived_project.archived
        with django_assert_num_queries(8):
            response = user_client.post(resource_url)
            assert response.status_code == 200
        archived_project.refresh_from_db()
        assert not archived_project.archived

    def test_get_method_not_allowed(
        self, user_client: Client, resource_url: str, team_member: TeamMember
    ) -> None:
        """Test that GET requests are not allowed."""
        response = user_client.get(resource_url)
        assert response.status_code == 405

    def test_project_not_found(
        self, user_client: Client, team_member: TeamMember, null_uuid: UUID
    ) -> None:
        """Test recovering a non-existent project returns 404."""
        url = reverse("dashboard:projects:recover", args=(null_uuid,))
        response = user_client.post(url)
        assert response.status_code == 404

    def test_active_project_not_found(
        self, user_client: Client, project: Project, team_member: TeamMember
    ) -> None:
        """Test that active (non-archived) projects can't be recovered."""
        url = reverse("dashboard:projects:recover", args=(project.uuid,))
        response = user_client.post(url)
        assert response.status_code == 404

    def test_unauthorized_project_access(
        self, user_client: Client, unrelated_project: Project, now: datetime
    ) -> None:
        """Test that users can't recover projects they don't have access to."""
        unrelated_project.archived = now
        unrelated_project.save()
        url = reverse(
            "dashboard:projects:recover", args=(unrelated_project.uuid,)
        )
        response = user_client.post(url)
        assert response.status_code == 404


class TestProjectDeleteView:
    """Test html project delete view."""

    @pytest.fixture
    def resource_url(self, archived_project: Project) -> str:
        """Return URL to this view."""
        return reverse(
            "dashboard:projects:delete", args=(archived_project.uuid,)
        )

    def test_post_delete_project(
        self,
        user_client: Client,
        resource_url: str,
        archived_project: Project,
        team_member: TeamMember,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Test successfully deleting an archived project via HTMX."""
        project_uuid = archived_project.uuid
        assert archived_project.archived
        # Gone up from   7 -> 8 since we delete user preferences
        # Gone up from   8 -> 9
        # Gone down from 9 -> 8 after deleting the Section model
        # Gone up from   8 -> 10
        with django_assert_num_queries(10):
            response = user_client.post(resource_url)
            assert response.status_code == 200
        assert not Project.objects.filter(uuid=project_uuid).exists()

    def test_get_method_not_allowed(
        self, user_client: Client, resource_url: str, team_member: TeamMember
    ) -> None:
        """Test that GET requests are not allowed."""
        response = user_client.get(resource_url)
        assert response.status_code == 405

    def test_project_not_found(
        self, user_client: Client, team_member: TeamMember, null_uuid: UUID
    ) -> None:
        """Test deleting a non-existent project returns 404."""
        url = reverse("dashboard:projects:delete", args=(null_uuid,))
        response = user_client.post(url)
        assert response.status_code == 404

    def test_active_project_not_found(
        self, user_client: Client, project: Project, team_member: TeamMember
    ) -> None:
        """Test that active (non-archived) projects can't be deleted."""
        url = reverse("dashboard:projects:delete", args=(project.uuid,))
        response = user_client.post(url)
        assert response.status_code == 404

    def test_unauthorized_project_access(
        self, user_client: Client, unrelated_project: Project, now: datetime
    ) -> None:
        """Test that users can't delete projects they don't have access to."""
        unrelated_project.archived = now
        unrelated_project.save()
        url = reverse(
            "dashboard:projects:delete", args=(unrelated_project.uuid,)
        )
        response = user_client.post(url)
        assert response.status_code == 404
