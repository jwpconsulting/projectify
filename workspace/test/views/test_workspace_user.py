"""Test workspace user views."""
from django.urls import (
    reverse,
)

import pytest
from rest_framework import status
from rest_framework.test import (
    APIClient,
)

from pytest_types import DjangoAssertNumQueries

from ...models.workspace_user import (
    WorkspaceUser,
)


@pytest.mark.django_db
class TestWorkspaceUserReadUpdateDelete:
    """Test workspace user RUD."""

    @pytest.fixture
    def resource_url(self, workspace_user: WorkspaceUser) -> str:
        """Return the resource url to the fixture workspace user."""
        return reverse(
            "workspace:workspace-users:read-update-delete",
            args=(str(workspace_user.uuid),),
        )

    def test_read(
        self,
        rest_user_client: APIClient,
        resource_url: str,
        workspace_user: WorkspaceUser,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Test reading a user."""
        with django_assert_num_queries(2):
            response = rest_user_client.get(resource_url)
            assert response.status_code == status.HTTP_200_OK, response.data
        assert response.data["job_title"] == workspace_user.job_title

    def test_update(
        self,
        rest_user_client: APIClient,
        resource_url: str,
        workspace_user: WorkspaceUser,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Test reading a user."""
        with django_assert_num_queries(8):
            response = rest_user_client.put(
                resource_url,
                data={
                    "job_title": "World famous plumber from Brooklyn",
                    "role": "OBSERVER",
                },
            )
            assert response.status_code == status.HTTP_200_OK, response.data
        assert (
            response.data["job_title"] == "World famous plumber from Brooklyn"
        )

    def test_delete_self(
        self,
        rest_user_client: APIClient,
        resource_url: str,
    ) -> None:
        """Test that deleting oneself does not work."""
        response = rest_user_client.delete(resource_url)
        assert response.status_code == 400, response.data
        assert (
            response.data["workspace_user"]
            == "Can't delete own workspace user"
        )

    def test_delete_other(
        self,
        rest_user_client: APIClient,
        workspace_user: WorkspaceUser,
        other_workspace_user: WorkspaceUser,
    ) -> None:
        """Test deleting another user."""
        resource_url = reverse(
            "workspace:workspace-users:read-update-delete",
            args=(str(other_workspace_user.uuid),),
        )
        response = rest_user_client.delete(resource_url)
        assert response.status_code == 204, response.data
        # The second time, the user is now gone
        response = rest_user_client.delete(resource_url)
        assert response.status_code == 404, response.data
