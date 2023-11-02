"""Test workspace user views."""
from django.urls import (
    reverse,
)

import pytest
from rest_framework.test import (
    APIClient,
)

from workspace.factory import (
    WorkspaceUserFactory,
)

from ...models.workspace_user import (
    WorkspaceUser,
)


@pytest.mark.django_db
class TestWorkspaceUserDestroy:
    """Test task creation."""

    def test_delete_self(
        self,
        rest_user_client: APIClient,
        workspace_user: WorkspaceUser,
    ) -> None:
        """Test that deleting oneself does not work."""
        resource_url = reverse(
            "workspace:workspace-user-delete", args=(str(workspace_user.uuid),)
        )
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
    ) -> None:
        """Test deleting another user."""
        other = WorkspaceUserFactory.create(workspace=workspace_user.workspace)
        resource_url = reverse(
            "workspace:workspace-user-delete", args=(str(other.uuid),)
        )
        response = rest_user_client.delete(resource_url)
        assert response.status_code == 204, response.data
        # The second time, the user is now gone
        response = rest_user_client.delete(resource_url)
        assert response.status_code == 404, response.data
