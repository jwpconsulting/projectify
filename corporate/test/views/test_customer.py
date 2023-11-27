"""Test customer views."""
from django.urls import (
    reverse,
)

import pytest
from rest_framework.test import APIClient

from pytest_types import DjangoAssertNumQueries
from workspace.models.workspace import Workspace
from workspace.models.workspace_user import WorkspaceUser

from ...models import Customer


@pytest.mark.django_db
class TestWorkspaceCustomerRetrieve:
    """Test WorkspaceCustomerRetrieve."""

    @pytest.fixture
    def resource_url(self, customer: Customer, workspace: Workspace) -> str:
        """Return URL to resource."""
        return reverse("corporate:workspace-customer", args=(workspace.uuid,))

    def test_authenticated(
        self,
        user_client: APIClient,
        resource_url: str,
        workspace_user_customer: WorkspaceUser,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Test as authenticated user."""
        with django_assert_num_queries(8):
            response = user_client.get(resource_url)
            assert response.status_code == 200, response.content
