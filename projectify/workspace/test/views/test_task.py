# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023-2024 JWP Consulting GK
"""Test task CRUD views."""

import re
from uuid import UUID

from django.test.client import Client
from django.urls import reverse

import pytest

from pytest_types import DjangoAssertNumQueries

from ...models import Project, Task, TeamMember

pytestmark = pytest.mark.django_db


class TestTaskCreateView:
    """Test HTML task creation view."""

    @pytest.fixture
    def resource_url(self, project: Project) -> str:
        """Return URL to this view."""
        return reverse("dashboard:projects:create-task", args=(project.uuid,))

    def test_get_task_create(
        self,
        unrelated_user_client: Client,
        user_client: Client,
        resource_url: str,
        project: Project,
        team_member: TeamMember,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Test GETting the task creation page."""
        # Someone else can't access it
        assert unrelated_user_client.get(resource_url).status_code == 404
        with django_assert_num_queries(10):
            response = user_client.get(resource_url)
            assert response.status_code == 200
        assert project.title in response.content.decode()

    def test_create_task(
        self,
        user_client: Client,
        resource_url: str,
        team_member: TeamMember,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Test creating a task."""
        initial_task_count = Task.objects.count()
        t_uid = str(team_member.uuid)
        desc = "<p>Assigned Task</p><h1>Bar</h1><p>Qux</p>"
        data = {"description": desc, "assignee": t_uid, "action": "create"}
        with django_assert_num_queries(11):
            response = user_client.post(resource_url, data)
            assert response.status_code == 302, response.content

        assert Task.objects.count() == initial_task_count + 1
        task = Task.objects.get()
        assert task.assignee == team_member
        assert task.title == "Assigned Task"

    def test_create_task_title_extraction(
        self, user_client: Client, resource_url: str, team_member: TeamMember
    ) -> None:
        """Test setting the title."""
        t_uid = str(team_member.uuid)
        # No description
        data = {"assignee": t_uid, "action": "create"}
        response = user_client.post(resource_url, data)
        assert response.status_code == 400

        # Empty description
        data = {"assignee": t_uid, "action": "create", "description": ""}
        response = user_client.post(resource_url, data)
        assert response.status_code == 400

        # Empty-ish description
        data = {
            "assignee": t_uid,
            "action": "create",
            "description": "<p></p>",
        }
        response = user_client.post(resource_url, data)
        assert response.status_code == 400

    def test_project_not_found(
        self, user_client: Client, null_uuid: UUID
    ) -> None:
        """Test accessing task creation for non-existent project."""
        url = reverse("dashboard:projects:create-task", args=(null_uuid,))
        response = user_client.get(url)
        assert response.status_code == 404


class TestTaskUpdateView:
    """Test HTML task update view."""

    @pytest.fixture
    def resource_url(self, task: Task) -> str:
        """Return URL to this view."""
        return reverse("dashboard:tasks:update", args=(task.uuid,))

    def test_get_task_update(
        self,
        unrelated_user_client: Client,
        user_client: Client,
        resource_url: str,
        task: Task,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Test GETting the task update page."""
        # Someone else can't access it
        assert unrelated_user_client.get(resource_url).status_code == 404
        # Gone up   from 14 -> 16 due to permission checks in sidemenu
        # Gone down from 16 -> 13
        # Gone down from 13 -> 12
        # Gone down from 12 -> 11
        # Gone up   from 11 -> 13
        with django_assert_num_queries(13):
            response = user_client.get(resource_url)
            assert response.status_code == 200
        assert task.title in response.content.decode()

    def test_get_no_description(
        self, user_client: Client, resource_url: str, task: Task
    ) -> None:
        """Test getting the form when the task has no description."""
        task.description = ""
        task.save()
        response = user_client.get(resource_url)
        assert response.status_code == 200
        match = re.search(
            r'\<input name="description".+?value="(.+?)" />',
            response.content.decode(),
            re.DOTALL,
        )
        assert match is not None
        assert match.group(1) == task.title, match.group(0)

    def test_task_not_found(
        self, user_client: Client, null_uuid: UUID
    ) -> None:
        """Test accessing task update for non-existent task."""
        url = reverse("dashboard:tasks:update", args=(null_uuid,))
        response = user_client.get(url)
        assert response.status_code == 404

    def test_update_task(
        self,
        user_client: Client,
        resource_url: str,
        task: Task,
        team_member: TeamMember,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Test updating a task."""
        assert task.title != "Updated Task Title"
        desc = "<p>Updated Task Title</p><p>Rest</p>"
        t_uid = str(team_member.uuid)
        data = {"description": desc, "assignee": t_uid}
        with django_assert_num_queries(12):
            response = user_client.post(resource_url, data)
            assert response.status_code == 302
        task.refresh_from_db()
        assert task.title == "Updated Task Title"
        assert task.assignee == team_member

    def test_update_task_no_description(
        self, user_client: Client, resource_url: str, team_member: TeamMember
    ) -> None:
        """Assert that you have to give the task a title."""
        t_uid = str(team_member.uuid)
        data = {"description": "<p></p>", "assignee": t_uid}
        response = user_client.post(resource_url, data)
        assert response.status_code == 400, response.content
