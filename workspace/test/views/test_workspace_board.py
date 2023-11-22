"""Test workspace board CRUD views."""
from django.contrib.auth.models import (
    AbstractBaseUser,
)
from django.urls import (
    reverse,
)

import pytest
from rest_framework.test import (
    APIClient,
)

from pytest_types import (
    DjangoAssertNumQueries,
)
from workspace.models import TaskLabel, WorkspaceBoard
from workspace.models.task import Task
from workspace.models.workspace import Workspace
from workspace.models.workspace_user import WorkspaceUser


# Create
@pytest.mark.django_db
class TestWorkspaceBoardCreate:
    """Test workspace board creation."""

    @pytest.fixture
    def resource_url(self) -> str:
        """Return URL to this view."""
        return reverse("workspace:workspace-boards:create")

    def test_authenticated(
        self,
        user: AbstractBaseUser,
        rest_user_client: APIClient,
        resource_url: str,
        django_assert_num_queries: DjangoAssertNumQueries,
        workspace: Workspace,
        # Make sure that we are part of that workspace
        workspace_user: WorkspaceUser,
    ) -> None:
        """Assert that we can create a new workspace board."""
        with django_assert_num_queries(12):
            response = rest_user_client.post(
                resource_url,
                {
                    "title": "New workspace board, who dis??",
                    "workspace_uuid": str(workspace.uuid),
                },
            )
        assert response.status_code == 201
        assert WorkspaceBoard.objects.count() == 1
        workspace_board = WorkspaceBoard.objects.get()
        assert workspace_board.title == "New workspace board, who dis??"


# Retrieve
@pytest.mark.django_db
class TestWorkspaceBoardRead:
    """Test WorkspaceBoardRead view."""

    @pytest.fixture
    def resource_url(self, workspace_board: WorkspaceBoard) -> str:
        """Return URL to this view."""
        return reverse(
            "workspace:workspace-boards:read", args=(workspace_board.uuid,)
        )

    def test_authenticated(
        self,
        rest_user_client: APIClient,
        resource_url: str,
        user: AbstractBaseUser,
        workspace: Workspace,
        workspace_user: WorkspaceUser,
        task: Task,
        other_task: Task,
        task_label: TaskLabel,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Assert we can post to this view this while being logged in."""
        with django_assert_num_queries(7):
            response = rest_user_client.get(resource_url)
        assert response.status_code == 200, response.content
