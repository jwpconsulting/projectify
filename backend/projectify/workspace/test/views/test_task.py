# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023-2024 JWP Consulting GK
"""Test task CRUD views."""

from uuid import uuid4

from django.test.client import Client
from django.urls import reverse

import pytest
from rest_framework.response import Response
from rest_framework.test import APIClient

from projectify.workspace.models.section import Section
from projectify.workspace.models.task import Task
from pytest_types import DjangoAssertNumQueries

from ... import models
from ...services.sub_task import sub_task_create


class UnauthenticatedTestMixin:
    """Test that resource cannot be accessed without authorization."""

    def test_unauthenticated(
        self, resource_url: str, rest_client: APIClient
    ) -> None:
        """Test we cannot access the resource."""
        response: Response = rest_client.options(resource_url)
        # It's not 403, because DRF does not return the www authenticate realm
        # as a response to an API user.
        # See
        # https://github.com/encode/django-rest-framework/blob/605cc4f7367f58002056453d9befd3c1918f6a38/rest_framework/authentication.py#L112
        # there is no "authenticate_header" method. If it existed, we would
        # get a 401 instead. I was confused at first, but by their logic it
        # makes some sense.
        assert response.status_code == 403, response.data


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
        team_member: models.TeamMember,
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
        team_member: models.TeamMember,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Test creating a task."""
        initial_task_count = Task.objects.count()
        with django_assert_num_queries(27):
            response = user_client.post(
                resource_url,
                {
                    "title": "Assigned Task",
                    "assignee": str(team_member.uuid),
                    "action": "create",
                    "form-TOTAL_FORMS": "1",
                    "form-INITIAL_FORMS": "0",
                    "form-MIN_NUM_FORMS": "0",
                    "form-MAX_NUM_FORMS": "1000",
                    "form-0-title": "Test subtask",
                    "form-0-done": "False",
                },
            )
            assert response.status_code == 302

        assert Task.objects.count() == initial_task_count + 1
        task = Task.objects.get()
        assert task.assignee == team_member
        assert task.subtask_set.count() == 1
        subtask = task.subtask_set.get()
        assert subtask.title == "Test subtask"
        assert subtask.done is False

    def test_section_not_found(
        self, user_client: Client, team_member: models.TeamMember
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
        team_member: models.TeamMember,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Test updating a task."""
        original_title = task.title
        with django_assert_num_queries(27):
            response = user_client.post(
                resource_url,
                {
                    "title": "Updated Task Title",
                    "assignee": str(team_member.uuid),
                    "action": "update",
                    "form-TOTAL_FORMS": "1",
                    "form-INITIAL_FORMS": "0",
                    "form-MIN_NUM_FORMS": "0",
                    "form-MAX_NUM_FORMS": "1000",
                    "form-0-title": "Updated subtask",
                    "form-0-done": "True",
                },
            )
            assert response.status_code == 302

        task.refresh_from_db()
        assert task.title == "Updated Task Title"
        assert task.title != original_title
        assert task.assignee == team_member
        assert task.subtask_set.count() == 1
        subtask = task.subtask_set.get()
        assert subtask.title == "Updated subtask"
        assert subtask.done is True

    def test_add_subtask_to_existing_task(
        self,
        user_client: Client,
        resource_url: str,
        task: Task,
        team_member: models.TeamMember,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Test adding a subtask to a task that already has one."""
        sub_task_create(
            who=team_member.user,
            task=task,
            title="subtask",
            done=False,
        )
        assert task.subtask_set.count() == 1

        existing_subtask = task.subtask_set.get()

        with django_assert_num_queries(28):
            response = user_client.post(
                resource_url,
                {
                    "title": task.title,
                    "assignee": str(team_member.uuid),
                    "action": "update",
                    "form-TOTAL_FORMS": "3",
                    "form-INITIAL_FORMS": "1",
                    "form-MIN_NUM_FORMS": "0",
                    "form-MAX_NUM_FORMS": "1000",
                    # Existing subtask
                    "form-0-title": "subtask",
                    "form-0-done": "False",
                    "form-0-uuid": str(existing_subtask.uuid),
                    "form-0-delete": "False",
                    # Empty title so should be ignored
                    "form-1-title": "",
                    "form-1-done": "True",
                    # New subtask
                    "form-2-title": "New additional subtask",
                    "form-2-done": "True",
                },
            )
            assert response.status_code == 302, response.content

        task.refresh_from_db()
        assert task.subtask_set.count() == 2

        subtask_a, subtask_b = list(task.subtask_set.all())

        assert subtask_a.title == "subtask"
        assert subtask_a.done is False
        assert subtask_b.title == "New additional subtask"
        assert subtask_b.done is True

    def test_delete_existing_subtask(
        self,
        user_client: Client,
        resource_url: str,
        task: Task,
        team_member: models.TeamMember,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Test marking an existing subtask for deletion."""
        subtask = sub_task_create(
            who=team_member.user, task=task, title="subtask", done=False
        )
        assert task.subtask_set.count() == 1

        with django_assert_num_queries(26):
            response = user_client.post(
                resource_url,
                {
                    "title": task.title,
                    "assignee": str(team_member.uuid),
                    "action": "update",
                    "form-TOTAL_FORMS": "1",
                    "form-INITIAL_FORMS": "1",
                    "form-MIN_NUM_FORMS": "0",
                    "form-MAX_NUM_FORMS": "1000",
                    # Mark existing subtask for deletion
                    "form-0-title": "subtask",
                    "form-0-done": "False",
                    "form-0-uuid": str(subtask.uuid),
                    "form-0-delete": "True",
                },
            )
            assert response.status_code == 302

        task.refresh_from_db()
        assert task.subtask_set.count() == 0
