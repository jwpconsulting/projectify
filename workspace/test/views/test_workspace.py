"""Test workspace CRUD views."""
from django.contrib.auth.models import (
    AbstractBaseUser,
    AbstractUser,
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
from rest_framework import status
from rest_framework.test import (
    APIClient,
)

from pytest_types import (
    DjangoAssertNumQueries,
    Headers,
)

from ... import (
    models,
)


# Create
@pytest.mark.django_db
class TestWorkspaceCreate:
    """Test workspace create."""

    @pytest.fixture
    def resource_url(self) -> str:
        """Return URL to this view."""
        return reverse("workspace:workspace-create")

    def test_authenticated(
        self,
        user: AbstractBaseUser,
        rest_user_client: APIClient,
        resource_url: str,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Assert that we can create a new workspace."""
        with django_assert_num_queries(2):
            response = rest_user_client.post(
                resource_url,
                {
                    "title": "New workspace, who dis?",
                    "description": "Synergize vertical integration in Q4",
                },
            )
            assert response.status_code == 201
        assert models.Workspace.objects.count() == 1
        workspace = models.Workspace.objects.get()
        workspace_user = workspace.workspaceuser_set.get()
        assert workspace_user.user == user
        assert workspace_user.role == "OWNER"


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
class TestWorkspaceReadUpdate:
    """Test WorkspaceReadUpdate."""

    @pytest.fixture
    def resource_url(self, workspace: models.Workspace) -> str:
        """Return URL to this view."""
        return reverse(
            "workspace:workspaces:read-update", args=(workspace.uuid,)
        )

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

    def test_updating(
        self,
        rest_user_client: APIClient,
        resource_url: str,
        user: AbstractBaseUser,
        workspace: models.Workspace,
        workspace_user: models.WorkspaceUser,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Test updating a given workspace with a new title."""
        with django_assert_num_queries(11):
            response = rest_user_client.put(
                resource_url,
                data={
                    "title": "New title",
                },
            )
        assert response.status_code == status.HTTP_200_OK, response.data
        workspace.refresh_from_db()
        assert workspace.title == "New title"


# Delete


# RPC
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


@pytest.mark.django_db
class TestInviteUserToWorkspace:
    """Test InviteUserToWorkspace."""

    @pytest.fixture
    def resource_url(self, workspace_user: models.WorkspaceUser) -> str:
        """Return URL to this view."""
        return reverse(
            "workspace:workspace-invite-user",
            # Using the workspace_user fixture, we create a ws user and ws in
            # one go! Mighty clever I dare say >:)
            args=(workspace_user.workspace.uuid,),
        )

    def test_new_user(
        self,
        resource_url: str,
        user_client: Client,
        workspace: models.Workspace,
    ) -> None:
        """Test with a new, unregistered user."""
        assert workspace.workspaceuserinvite_set.count() == 0
        response = user_client.post(
            resource_url,
            {"email": "taro@yamamoto.jp"},
        )
        assert response.status_code == 201, response.content
        assert workspace.workspaceuserinvite_set.count() == 1

    def test_existing_user(
        self,
        resource_url: str,
        user_client: Client,
        workspace: models.Workspace,
        other_user: AbstractUser,
    ) -> None:
        """Test by inviting an existing user."""
        assert workspace.workspaceuserinvite_set.count() == 0
        response = user_client.post(
            resource_url,
            {"email": other_user.email},
        )
        assert response.status_code == 201, response.content
        assert workspace.workspaceuserinvite_set.count() == 0

    def test_existing_workspace_user(
        self,
        resource_url: str,
        rest_user_client: APIClient,
        workspace_user: models.WorkspaceUser,
    ) -> None:
        """Test inviting an existing workspace user."""
        response = rest_user_client.post(
            resource_url,
            {"email": workspace_user.user.email},
        )
        assert response.status_code == 400, response.data
        assert "already been added" in response.data["email"], response.data

    def test_existing_invitation(
        self, resource_url: str, rest_user_client: APIClient
    ) -> None:
        """Test inviting someone twice."""
        response = rest_user_client.post(
            resource_url,
            {"email": "hello@example.com"},
        )
        assert response.status_code == 201, response.content
        response = rest_user_client.post(
            resource_url,
            {"email": "hello@example.com"},
        )
        assert response.status_code == 400, response.data
        assert "already been invited" in response.data["email"], response.data
