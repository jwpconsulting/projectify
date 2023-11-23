"""Test label views."""
from django.urls import reverse

import pytest
from rest_framework.test import APIClient

from pytest_types import DjangoAssertNumQueries
from workspace.models.workspace import Workspace
from workspace.models.workspace_user import WorkspaceUser


@pytest.mark.django_db
class TestLabelCreate:
    """Test label creation."""

    @pytest.fixture
    def resource_url(self) -> str:
        """Return URL to this view."""
        return reverse("workspace:labels:create")

    def test_authenticated_user(
        self,
        rest_user_client: APIClient,
        resource_url: str,
        django_assert_num_queries: DjangoAssertNumQueries,
        workspace: Workspace,
        # Make sure we have a user
        workspace_user: WorkspaceUser,
    ) -> None:
        """Test as an authenticated user."""
        with django_assert_num_queries(10):
            response = rest_user_client.post(
                resource_url,
                data={
                    "color": 0,
                    "name": "Bug",
                    "workspace_uuid": str(workspace.uuid),
                },
            )
        assert response.status_code == 201, response.data
        assert response.data["name"] == "Bug"
