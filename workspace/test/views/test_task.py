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
            "workspace_board_section": workspace_board_section.uuid,
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
        assert models.Task.objects.count() == 0

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
        with django_assert_num_queries(34):
            response = rest_user_client.post(
                resource_url,
                {**payload, "assignee": workspace_user.uuid},
                format="json",
            )
            assert response.status_code == 201, response.data
        assert models.Task.objects.count() == 1
        assert models.Task.objects.get().assignee == workspace_user


# Read
@pytest.mark.django_db
class TestTaskRetrieve(UnauthenticatedTestMixin):
    """Test Task retrieve."""

    @pytest.fixture
    def resource_url(self, task: models.Task) -> str:
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
            "workspace_board_section": workspace_board_section.uuid,
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
        with django_assert_num_queries(33):
            response = rest_user_client.put(
                resource_url,
                {**payload, "assignee": workspace_user.uuid},
                format="json",
            )
            assert response.status_code == 200, response.content
        assert response.data["title"] == "Hello world"
        # We get the whole nested thing
        assert (
            response.data["workspace_board_section"]["title"]
            == workspace_board_section.title
        )


# Delete
