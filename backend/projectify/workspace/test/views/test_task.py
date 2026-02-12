# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023-2024 JWP Consulting GK
"""Test task CRUD views."""

from uuid import uuid4

from django.urls import reverse

import pytest
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient

from projectify.workspace.models.section import Section
from projectify.workspace.models.task import Task
from pytest_types import DjangoAssertNumQueries

from ... import models


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


# Create
@pytest.mark.django_db
class TestTaskCreate(UnauthenticatedTestMixin):
    """Test task creation."""

    @pytest.fixture
    def resource_url(self) -> str:
        """Return URL to resource."""
        return reverse("workspace:tasks:create")

    @pytest.fixture
    def payload(
        self,
        section: models.Section,
    ) -> dict[str, object]:
        """Return a payload for API."""
        return {
            "title": "bla",
            "description": None,
            "labels": [],
            "assignee": None,
            "section": {"uuid": str(section.uuid)},
            "sub_tasks": [
                {"title": "I am a sub task", "done": False},
            ],
            "due_date": None,
        }

    def test_unauthorized(
        self,
        rest_meddling_client: APIClient,
        resource_url: str,
        payload: dict[str, object],
    ) -> None:
        """Test creating when unauthorized."""
        response = rest_meddling_client.post(
            resource_url, payload, format="json"
        )
        # We get 400 and NOT 403. We don't want to tell the user whether a
        # section with the given UUID exists. Instead, we
        # will treat it like a non-existent UUID. That makes sense, because to
        # the user it *really* does not exist and anything else does not
        # matter.
        assert response.status_code == 400, response.data
        assert response.data == {
            "status": "invalid",
            "code": 400,
            "details": {"section": "Section does not exist"},
            "general": None,
        }
        assert Task.objects.count() == 0

    def test_authenticated(
        self,
        rest_user_client: APIClient,
        resource_url: str,
        team_member: models.TeamMember,
        django_assert_num_queries: DjangoAssertNumQueries,
        payload: dict[str, object],
    ) -> None:
        """Test creating when authenticated."""
        # 6 queries just for assigning a user
        # TODO We are going from 34 -> 44 queries. This means an increase of 9
        # queries after we started firing a signal after serializer.save()
        # The increase below for RetrieveUpdate was only 7. Maybe we can look
        # into where the additional 3 queries on top of the 7 come. It could be
        # somethign we failed to select or prefetch.
        # XXX Justus 2024-01-11 went up to 22 now, but since we are refactoring
        # signals, this might change up so I will ignore this for now
        # 25 now
        # 26 now
        # 24 now
        # 21 now Justus 2024-05-23
        with django_assert_num_queries(25):
            response = rest_user_client.post(
                resource_url,
                {**payload, "assignee": {"uuid": str(team_member.uuid)}},
                format="json",
            )
            assert response.status_code == 201, response.data
        assert Task.objects.count() == 1
        assert Task.objects.get().assignee == team_member

    def test_error_format(
        self,
        rest_user_client: APIClient,
        resource_url: str,
        team_member: models.TeamMember,
        payload: dict[str, object],
    ) -> None:
        """Test nested error serialization."""
        payload = {
            **payload,
            "sub_tasks": [
                {"done": "hello", "title": "I am sub task"},
                {"done": True, "title": None},
            ],
        }
        response = rest_user_client.post(
            resource_url,
            {**payload, "assignee": {"uuid": str(team_member.uuid)}},
            format="json",
        )
        assert response.status_code == 400, response.data
        assert response.data == {
            "status": "invalid",
            "code": 400,
            "details": {
                "sub_tasks": [
                    {"done": "Must be a valid boolean."},
                    {"title": "This field may not be null."},
                ]
            },
            "general": None,
        }


# Read
@pytest.mark.django_db
class TestTaskRetrieveUpdateDestroy(UnauthenticatedTestMixin):
    """Test Task read, update and delete."""

    @pytest.fixture
    def resource_url(self, task: Task) -> str:
        """Return URL to resource."""
        return reverse("workspace:tasks:read-update-delete", args=(task.uuid,))

    @pytest.fixture
    def payload(self) -> dict[str, object]:
        """Create payload."""
        return {
            "title": "Hello world",
            "description": None,
            "number": 2,
            "labels": [],
            "assignee": None,
            "due_date": None,
        }

    def test_unauthorized(
        self,
        rest_meddling_client: APIClient,
        resource_url: str,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Test retrieving when logged in, but not authorized."""
        with django_assert_num_queries(1):
            response = rest_meddling_client.get(resource_url)
            assert response.status_code == 404, response.data

    def test_authenticated(
        self,
        rest_user_client: APIClient,
        resource_url: str,
        team_member: models.TeamMember,
        task: Task,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Test retrieving when authenticated."""
        # Gone up from 5 -> 9, since we added filtering annotations
        with django_assert_num_queries(9):
            response = rest_user_client.get(resource_url)
            assert response.status_code == 200, response.data

        assert response.data["uuid"] == str(task.uuid)

    def test_update(
        self,
        rest_user_client: APIClient,
        resource_url: str,
        django_assert_num_queries: DjangoAssertNumQueries,
        team_member: models.TeamMember,
        section: models.Section,
        payload: dict[str, object],
    ) -> None:
        """Test updating a task when logged in correctly."""
        # XXX high query count but ignore for now
        # 29 now
        # 31 now
        # 28 now
        # 22 now
        # Gone up from 24 -> 31, since we added filtering annotations
        with django_assert_num_queries(31):
            response = rest_user_client.put(
                resource_url,
                {**payload, "assignee": {"uuid": str(team_member.uuid)}},
                format="json",
            )
            assert response.status_code == 200, response.content
        assert response.data["title"] == "Hello world"
        # We get the whole nested thing
        assert response.data["section"]["title"] == section.title

    def test_update_error_format(
        self,
        rest_user_client: APIClient,
        resource_url: str,
        django_assert_num_queries: DjangoAssertNumQueries,
        team_member: models.TeamMember,
        payload: dict[str, object],
    ) -> None:
        """Test updating a task when logged in correctly."""
        # Gone up from 5 -> 6, since we added filtering annotations
        with django_assert_num_queries(6):
            response = rest_user_client.put(
                resource_url,
                {
                    **payload,
                    "sub_tasks": [
                        {"uuid": str(uuid4()), "title": "bla", "done": False}
                    ],
                    "assignee": {"uuid": str(team_member.uuid)},
                },
                format="json",
            )
        assert response.status_code == 400
        assert response.data == {
            "code": 400,
            "status": "invalid",
            "details": {
                "sub_tasks": [{}],
            },
            "general": None,
        }

    def test_delete(
        self,
        rest_user_client: APIClient,
        resource_url: str,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Test deleting a task."""
        # Gone up from 11 -> 13, since we added filtering annotations
        with django_assert_num_queries(13):
            response = rest_user_client.delete(resource_url)
            assert response.status_code == 204, response.content
        # Ensure that the task is gone for good
        with django_assert_num_queries(1):
            response = rest_user_client.get(resource_url)
            assert response.status_code == 404, response.content


# RPC
@pytest.mark.django_db
class TestMoveTaskToSection:
    """Test moving a task to a section."""

    @pytest.fixture
    def resource_url(self, task: Task) -> str:
        """Return URL to this view."""
        return reverse(
            "workspace:tasks:move-to-section",
            args=(str(task.uuid),),
        )

    def test_simple(
        self,
        rest_user_client: APIClient,
        resource_url: str,
        django_assert_num_queries: DjangoAssertNumQueries,
        section: Section,
        other_section: Section,
        task: Task,
    ) -> None:
        """Test moving a task."""
        assert task.section == section
        # Gone up from 19 -> 23, since we added filtering annotations
        with django_assert_num_queries(23):
            response = rest_user_client.post(
                resource_url,
                data={"section_uuid": str(other_section.uuid)},
            )
            assert response.status_code == status.HTTP_200_OK, response.data

        task.refresh_from_db()
        assert task.section == other_section
        assert task._order == 0


@pytest.mark.django_db
class TestTaskMoveAfterTask:
    """Test moving a task."""

    @pytest.fixture
    def resource_url(self, task: Task) -> str:
        """Return URL to this view."""
        return reverse(
            "workspace:tasks:move-after-task",
            args=(str(task.uuid),),
        )

    def test_simple(
        self,
        rest_user_client: APIClient,
        resource_url: str,
        django_assert_num_queries: DjangoAssertNumQueries,
        other_task: Task,
    ) -> None:
        """Test as an authenticated user."""
        # Gone up from 18 -> 22, since we added filtering annotations
        with django_assert_num_queries(22):
            response = rest_user_client.post(
                resource_url,
                data={"task_uuid": str(other_task.uuid)},
            )
            assert response.status_code == status.HTTP_200_OK, response.data
