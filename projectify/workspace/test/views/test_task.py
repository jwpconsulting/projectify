# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023-2024 JWP Consulting GK
"""Test task CRUD views."""

from uuid import uuid4

from django.test.client import Client
from django.urls import reverse

import pytest

from pytest_types import DjangoAssertNumQueries

from ...models import Section, Task, TeamMember

pytestmark = pytest.mark.django_db


class TestTaskCreateView:
    """Test HTML task creation view."""

    @pytest.fixture
    def resource_url(self, section: Section) -> str:
        """Return URL to this view."""
        return reverse("dashboard:sections:create-task", args=(section.uuid,))

    def test_get_task_create(
        self,
        user_client: Client,
        resource_url: str,
        section: Section,
        team_member: TeamMember,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Test GETting the task creation page."""
        with django_assert_num_queries(11):
            response = user_client.get(resource_url)
            assert response.status_code == 200
        assert section.title in response.content.decode()

    def test_create_task(
        self,
        user_client: Client,
        resource_url: str,
        team_member: TeamMember,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Test creating a task."""
        initial_task_count = Task.objects.count()
        with django_assert_num_queries(21):
            response = user_client.post(
                resource_url,
                {
                    "title": "Assigned Task",
                    "assignee": str(team_member.uuid),
                    "action": "create",
                },
            )
            assert response.status_code == 302

        assert Task.objects.count() == initial_task_count + 1
        task = Task.objects.get()
        assert task.assignee == team_member

    def test_section_not_found(
        self, user_client: Client, team_member: TeamMember
    ) -> None:
        """Test accessing task creation for non-existent section."""
        url = reverse("dashboard:sections:create-task", args=(uuid4(),))
        response = user_client.get(url)
        assert response.status_code == 404

    def test_unauthorized_section_access(
        self, user_client: Client, unrelated_section: Section
    ) -> None:
        """Test that users can't create tasks in sections they don't have access to."""
        url = reverse(
            "dashboard:sections:create-task", args=(unrelated_section.uuid,)
        )
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
        user_client: Client,
        resource_url: str,
        task: Task,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Test GETting the task update page."""
        with django_assert_num_queries(15):
            response = user_client.get(resource_url)
            assert response.status_code == 200
        assert task.title in response.content.decode()

    def test_task_not_found(self, user_client: Client) -> None:
        """Test accessing task update for non-existent task."""
        url = reverse("dashboard:tasks:update", args=(uuid4(),))
        response = user_client.get(url)
        assert response.status_code == 404

    def test_unauthorized_task_access(
        self, user_client: Client, unrelated_task: Task
    ) -> None:
        """Test that users can't update tasks they don't have access to."""
        url = reverse("dashboard:tasks:update", args=(unrelated_task.uuid,))
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
        original_title = task.title
        with django_assert_num_queries(25):
            response = user_client.post(
                resource_url,
                {
                    "title": "Updated Task Title",
                    "assignee": str(team_member.uuid),
                    "action": "update",
                },
            )
            assert response.status_code == 302

        task.refresh_from_db()
        assert task.title == "Updated Task Title"
        assert task.title != original_title
        assert task.assignee == team_member
