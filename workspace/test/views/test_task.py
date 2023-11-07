"""Test task CRUD views."""
from django.urls import (
    reverse,
)

import pytest
from rest_framework.response import (
    Response,
)
from rest_framework.test import (
    APIClient,
)

from pytest_types import (
    DjangoAssertNumQueries,
)
from workspace.models.task import (
    Task,
)

from ... import (
    models,
)


class UnauthenticatedTestMixin:
    """Test that resource cannot be accessed without authorization."""

    def test_unauthenticated(
        self, resource_url: str, test_client: APIClient
    ) -> None:
        """Test we cannot access the resource."""
        response: Response = test_client.options(resource_url)
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
        return reverse("workspace:task-create")

    @pytest.fixture
    def payload(
        self,
        workspace_board_section: models.WorkspaceBoardSection,
    ) -> dict[str, object]:
        """Return a payload for API."""
        return {
            "title": "bla",
            "labels": [],
            "assignee": None,
            "workspace_board_section": {
                "uuid": str(workspace_board_section.uuid)
            },
            "sub_tasks": [
                {"title": "I am a sub task", "done": False},
            ],
        }

    def test_unauthorized(
        self,
        rest_user_client: APIClient,
        resource_url: str,
        payload: dict[str, object],
    ) -> None:
        """Test creating when unauthorized."""
        response = rest_user_client.post(resource_url, payload, format="json")
        # We get 400 and NOT 403. We don't want to tell the user whether a
        # workspace board section with the given UUID exists. Instead, we
        # will treat it like a non-existent UUID. That makes sense, because to
        # the user it *really* does not exist and anything else does not
        # matter.
        assert response.status_code == 400, response.data
        assert Task.objects.count() == 0

    def test_authenticated(
        self,
        rest_user_client: APIClient,
        resource_url: str,
        workspace_user: models.WorkspaceUser,
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
        with django_assert_num_queries(44):
            response = rest_user_client.post(
                resource_url,
                {**payload, "assignee": {"uuid": str(workspace_user.uuid)}},
                format="json",
            )
            assert response.status_code == 201, response.data
        assert Task.objects.count() == 1
        assert Task.objects.get().assignee == workspace_user


# Read
@pytest.mark.django_db
class TestTaskRetrieveUpdateDestroy(UnauthenticatedTestMixin):
    """Test Task read, update and delete."""

    @pytest.fixture
    def resource_url(self, task: Task) -> str:
        """Return URL to resource."""
        return reverse("workspace:task", args=(task.uuid,))

    @pytest.fixture
    def payload(
        self,
        workspace_board_section: models.WorkspaceBoardSection,
    ) -> dict[str, object]:
        """Create payload."""
        return {
            "title": "Hello world",
            "workspace_board_section": {
                "uuid": str(workspace_board_section.uuid)
            },
            "number": 2,
            "labels": [],
            "assignee": None,
        }

    def test_unauthorized(
        self,
        rest_user_client: APIClient,
        resource_url: str,
        django_assert_num_queries: DjangoAssertNumQueries,
        workspace_user: models.WorkspaceUser,
        workspace: models.Workspace,
    ) -> None:
        """Test retrieving when logged in, but not authorized."""
        workspace.remove_user(workspace_user.user)
        with django_assert_num_queries(1):
            response = rest_user_client.get(resource_url)
        assert response.status_code == 404, response.data

    def test_authenticated(
        self,
        rest_user_client: APIClient,
        resource_url: str,
        workspace_user: models.WorkspaceUser,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Test retrieving when authenticated."""
        with django_assert_num_queries(4):
            response = rest_user_client.get(resource_url)
            assert response.status_code == 200, response.data

        assert response.data["assignee"]["uuid"] == str(workspace_user.uuid)

    def test_update(
        self,
        rest_user_client: APIClient,
        resource_url: str,
        django_assert_num_queries: DjangoAssertNumQueries,
        workspace_user: models.WorkspaceUser,
        workspace_board_section: models.WorkspaceBoardSection,
        payload: dict[str, object],
    ) -> None:
        """Test updating a task when logged in correctly."""
        # TODO so many queries...
        # TODO omg so many queries (22 -> 28)
        # TODO even more queries (28 -> 29)
        # TODO it's even more now, but the data is more complete (29 -> 33)
        # TODO because of the signal, there are 7 more (33 -> 40)
        # TODO would make sense to have the signal perform the additional
        # queries in the background... or is that already happening and testing
        # channels in memory we eagerly execute the tasks?
        with django_assert_num_queries(40):
            response = rest_user_client.put(
                resource_url,
                {**payload, "assignee": {"uuid": str(workspace_user.uuid)}},
                format="json",
            )
            assert response.status_code == 200, response.content
        assert response.data["title"] == "Hello world"
        # We get the whole nested thing
        assert (
            response.data["workspace_board_section"]["title"]
            == workspace_board_section.title
        )

    def test_delete(
        self,
        rest_user_client: APIClient,
        resource_url: str,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Test deleting a task."""
        with django_assert_num_queries(10):
            response = rest_user_client.delete(resource_url)
            assert response.status_code == 204, response.content
        # Ensure that the task is gone for good
        with django_assert_num_queries(1):
            response = rest_user_client.get(resource_url)
            assert response.status_code == 404, response.content
