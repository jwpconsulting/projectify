"""Test workspace views."""
import contextlib
from collections.abc import (
    Mapping,
)
from typing import (
    Any,
    Callable,
)

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

from .. import (
    models,
)


Headers = Mapping[str, Any]
DjangoAssertNumQueries = Callable[
    [int], contextlib.AbstractContextManager[None]
]


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
    ) -> None:
        """Assert wecan't view this while being logged out."""
        response = client.post(resource_url, **headers)
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
class TestWorkspaceBoardRetrieve:
    """Test WorkspaceBoardRetrieve view."""

    @pytest.fixture
    def resource_url(self, workspace_board: models.WorkspaceBoard) -> str:
        """Return URL to this view."""
        return reverse(
            "workspace:workspace-board", args=(workspace_board.uuid,)
        )

    def test_authenticated(
        self,
        user_client: Client,
        resource_url: str,
        user: AbstractBaseUser,
        workspace: models.Workspace,
        workspace_user: models.WorkspaceUser,
        task: models.Task,
        other_task: models.Task,
        task_label: models.TaskLabel,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Assert we can post to this view this while being logged in."""
        with django_assert_num_queries(9):
            response = user_client.get(resource_url)
        assert response.status_code == 200, response.content


@pytest.mark.django_db
class TestWorkspaceBoardSectionRetrieve:
    """Test WorkspaceBoardSectionRetrieve view."""

    @pytest.fixture
    def resource_url(
        self, workspace_board_section: models.WorkspaceBoardSection
    ) -> str:
        """Return URL to this view."""
        return reverse(
            "workspace:workspace-board-section",
            args=(workspace_board_section.uuid,),
        )

    def test_authenticated(
        self,
        user_client: Client,
        resource_url: str,
        user: AbstractBaseUser,
        workspace: models.Workspace,
        workspace_user: models.WorkspaceUser,
        task: models.Task,
        other_task: models.Task,
        task_label: models.TaskLabel,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Assert we can post to this view this while being logged in."""
        with django_assert_num_queries(8):
            response = user_client.get(resource_url)
        assert response.status_code == 200, response.content


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


@pytest.mark.django_db
class TestTaskRetrieve:
    """Test Task retrieve."""

    @pytest.fixture
    def resource_url(self, task: models.Task) -> str:
        """Return URL to resource."""
        return reverse("workspace:task", args=(task.uuid,))

    def test_authenticated(
        self,
        user_client: Client,
        resource_url: str,
        user: AbstractBaseUser,
        task: models.Task,
        workspace_user: models.WorkspaceUser,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Test retrieving when authenticated."""
        with django_assert_num_queries(6):
            response = user_client.get(resource_url)
        assert response.status_code == 200, response.content


@pytest.mark.django_db
class TestWorkspaceBoardsArchivedList:
    """Test WorkspaceBoardsArchived list."""

    @pytest.fixture
    def resource_url(self, workspace: models.Workspace) -> str:
        """Return URL to this view."""
        return reverse(
            "workspace:workspace-boards-archived", args=(workspace.uuid,)
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
        with django_assert_num_queries(4):
            response = user_client.get(resource_url)
        assert response.status_code == 200, response.content
        assert len(response.json()) == 1
