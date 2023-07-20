"""Test workspace views."""
from django.contrib.auth.models import (
    AbstractBaseUser,
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
)

from .. import (
    models,
)


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
