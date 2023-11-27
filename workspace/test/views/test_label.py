"""Test label views."""
from django.urls import reverse

import pytest
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.test import APIClient

from pytest_types import DjangoAssertNumQueries
from workspace.models.label import Label
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


@pytest.mark.django_db
class TestLabelUpdateDelete:
    """Test updating and deleting labels."""

    @pytest.fixture
    def resource_url(self, label: Label) -> str:
        """Return URL to this view."""
        return reverse(
            "workspace:labels:update-delete", args=(str(label.uuid),)
        )

    def test_authenticated_user(
        self,
        rest_user_client: APIClient,
        resource_url: str,
        django_assert_num_queries: DjangoAssertNumQueries,
        workspace_user: WorkspaceUser,
        label: Label,
    ) -> None:
        """Test as an authenticated user."""
        with django_assert_num_queries(11):
            response = rest_user_client.put(
                resource_url,
                data={
                    "color": 2,
                    "name": "New name for a label",
                },
            )
            assert response.status_code == 200, response.data
        label.refresh_from_db()
        assert label.name == "New name for a label"
        assert label.color == 2
        assert response.data["name"] == "New name for a label"

    def test_deleting(
        self,
        rest_user_client: APIClient,
        resource_url: str,
        django_assert_num_queries: DjangoAssertNumQueries,
        workspace_user: WorkspaceUser,
        label: Label,
    ) -> None:
        """Test deleting a label."""
        with django_assert_num_queries(12):
            response = rest_user_client.delete(resource_url)
            assert response.status_code == HTTP_204_NO_CONTENT, response.data
        assert Label.objects.count() == 0
