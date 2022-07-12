"""Test workspace views."""
from django.urls import (
    reverse,
)

import pytest


@pytest.mark.django_db
class TestWorkspacePictureUploadView:
    """Test WorkspacePictureUploadView."""

    @pytest.fixture
    def resource_url(self, workspace):
        """Return URL to this view."""
        return reverse(
            "workspace:workspace-picture-upload", args=(workspace.uuid,)
        )

    @pytest.fixture
    def headers(self, png_image):
        """Return headers."""
        return {
            "HTTP_CONTENT_DISPOSITION": "attachment; filename=test.png",
            "HTTP_CONTENT_LENGTH": len(png_image),
        }

    def test_unauthenticated(self, client, resource_url, headers):
        """Assert wecan't view this while being logged out."""
        response = client.post(resource_url, **headers)
        assert response.status_code == 403, response.content

    def test_authenticated(
        self,
        user_client,
        resource_url,
        headers,
        uploaded_file,
        user,
        workspace,
        workspace_user,
    ):
        """Assert we can post to this view this while being logged in."""
        response = user_client.post(
            resource_url,
            {"file": uploaded_file},
            format="multipart",
            **headers,
        )
        assert response.status_code == 204, response.content
        user.refresh_from_db()
        assert user.profile_picture is not None


@pytest.mark.django_db
class TestWorkspaceBoardRetrieve:
    """Test WorkspaceBoardRetrieve view."""

    @pytest.fixture
    def resource_url(self, workspace_board):
        """Return URL to this view."""
        return reverse(
            "workspace:workspace-board", args=(workspace_board.uuid,)
        )

    def test_authenticated(
        self,
        user_client,
        resource_url,
        user,
        workspace,
        workspace_user,
        task,
        other_task,
        task_label,
        django_assert_num_queries,
    ):
        """Assert we can post to this view this while being logged in."""
        with django_assert_num_queries(8):
            response = user_client.get(resource_url)
        assert response.status_code == 200, response.content


@pytest.mark.django_db
class TestWorkspaceRetrieveView:
    """Test WorkspaceRetrieve view."""

    @pytest.fixture
    def resource_url(self, workspace):
        """Return URL to this view."""
        return reverse("workspace:workspace", args=(workspace.uuid,))

    def test_authenticated(
        self,
        user_client,
        resource_url,
        user,
        workspace,
        workspace_user,
        workspace_board,
        django_assert_num_queries,
    ):
        """Assert we can GET this view this while being logged in."""
        with django_assert_num_queries(6):
            response = user_client.get(resource_url)
        assert response.status_code == 200, response.content
        assert len(response.json()["workspace_boards"]) == 1


@pytest.mark.django_db
class TestWorkspaceBoardsArchivedList:
    """Test WorkspaceBoardsArchived list."""

    @pytest.fixture
    def resource_url(self, workspace):
        """Return URL to this view."""
        return reverse(
            "workspace:workspace-boards-archived", args=(workspace.uuid,)
        )

    def test_authenticated(
        self,
        user_client,
        resource_url,
        user,
        workspace,
        workspace_user,
        workspace_board,
        archived_workspace_board,
        django_assert_num_queries,
    ):
        """Assert we can GET this view this while being logged in."""
        with django_assert_num_queries(4):
            response = user_client.get(resource_url)
        assert response.status_code == 200, response.content
        assert len(response.json()) == 1
