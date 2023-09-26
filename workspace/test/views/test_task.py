"""Test task CRUD views."""
from django.contrib.auth.models import (
    AbstractBaseUser,
)
from django.urls import (
    reverse,
)

import pytest
from rest_framework.test import (
    APIClient,
)

from pytest_types import (
    DjangoAssertNumQueries,
)

from ... import (
    models,
)


# Create
# Read
@pytest.mark.django_db
class TestTaskRetrieve:
    """Test Task retrieve."""

    @pytest.fixture
    def resource_url(self, task: models.Task) -> str:
        """Return URL to resource."""
        return reverse("workspace:task", args=(task.uuid,))

    def test_authenticated(
        self,
        rest_user_client: APIClient,
        resource_url: str,
        user: AbstractBaseUser,
        task: models.Task,
        workspace_user: models.WorkspaceUser,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Test retrieving when authenticated."""
        with django_assert_num_queries(4):
            response = rest_user_client.get(resource_url)
            assert response.status_code == 200, response.data

    def test_update(
        self,
        rest_user_client: APIClient,
        resource_url: str,
        task: models.Task,
        user: AbstractBaseUser,
        workspace_user: models.WorkspaceUser,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Assert we can GET this view this while being logged in."""
        data = {
            "title": "Hello world",
            "number": 2,
            "labels": [],
            "assignee": None,
        }
        # TODO so many queries...
        # TODO omg so many queries (22 -> 28)
        with django_assert_num_queries(28):
            response = rest_user_client.put(resource_url, data, format="json")
            assert response.status_code == 200, response.content
        assert response.data["title"] == "Hello world"


# Delete
