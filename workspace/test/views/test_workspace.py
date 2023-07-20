"""Test workspace CRUD views."""
from django.contrib.auth.models import (
    AbstractBaseUser,
)
from django.core.files import (
    File,
)
from django.test import (
    Client,
)
from django.urls import (
    reverse,
)

import pytest

from pytest_types import (
    DjangoAssertNumQueries,
    Headers,
)

from ... import (
    models,
)


# Create
# Read
@pytest.mark.django_db
class TestWorkspaceList:
    """Test Workspace list."""

    @pytest.fixture
    def resource_url(self) -> str:
        """Return URL to this view."""
        return reverse("workspace:workspace-list")

    def test_authenticated(
        self,
        user_client: Client,
        resource_url: str,
        user: AbstractBaseUser,
        workspace: models.Workspace,
        workspace_user: models.WorkspaceUser,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Assert we can GET this view this while being logged in."""
        with django_assert_num_queries(3):
            response = user_client.get(resource_url)
        assert response.status_code == 200, response.content
        assert len(response.json()) == 1


@pytest.mark.django_db
class TestWorkspaceRetrieveView:
    """Test WorkspaceRetrieve view."""

    @pytest.fixture
    def resource_url(self, workspace: models.Workspace) -> str:
        """Return URL to this view."""
        return reverse("workspace:workspace", args=(workspace.uuid,))

    def test_authenticated(
        self,
        user_client: Client,
        resource_url: str,
        user: AbstractBaseUser,
        workspace: models.Workspace,
        workspace_user: models.WorkspaceUser,
        workspace_board: models.WorkspaceBoard,
        archived_workspace_board: models.WorkspaceBoard,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Assert we can GET this view this while being logged in."""
        with django_assert_num_queries(6):
            response = user_client.get(resource_url)
        assert response.status_code == 200, response.content
        assert len(response.json()["workspace_boards"]) == 1


# Update
@pytest.mark.django_db
class TestWorkspacePictureUploadView:
    """Test WorkspacePictureUploadView."""

    @pytest.fixture
    def resource_url(self, workspace: models.Workspace) -> str:
        """Return URL to this view."""
        return reverse(
            "workspace:workspace-picture-upload", args=(workspace.uuid,)
        )

    @pytest.fixture
    def headers(self, png_image: File) -> Headers:
        """Return headers."""
        return {
            "HTTP_CONTENT_DISPOSITION": "attachment; filename=test.png",
            "HTTP_CONTENT_LENGTH": len(png_image),
        }

    def test_unauthenticated(
        self,
        client: Client,
        resource_url: str,
        headers: Headers,
        uploaded_file: File,
    ) -> None:
        """Assert we can't view this while being logged out."""
        response = client.post(
            resource_url,
            {"file": uploaded_file},
            format="multipart",
            **headers,
        )
        assert response.status_code == 403, response.content

    def test_authenticated(
        self,
        user_client: Client,
        resource_url: str,
        headers: Headers,
        uploaded_file: File,
        user: AbstractBaseUser,
        workspace: models.Workspace,
        workspace_user: models.WorkspaceUser,
    ) -> None:
        """Assert we can post to this view this while being logged in."""
        response = user_client.post(
            resource_url,
            {"file": uploaded_file},
            format="multipart",
            **headers,
        )
        assert response.status_code == 204, response.content
        workspace.refresh_from_db()
        assert workspace.picture is not None


# Delete
