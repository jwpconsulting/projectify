"""Test workspace board CRUD views."""
from django.contrib.auth.models import (
    AbstractBaseUser,
)
from django.urls import (
    reverse,
)
from django.utils.timezone import now

import pytest
from rest_framework import status
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


# Read + Update + Delete
@pytest.mark.django_db
class TestWorkspaceBoardReadUpdateDelete:
    """Test WorkspaceBoardReadUpdateDelete view."""

    @pytest.fixture
    def resource_url(self, workspace_board: WorkspaceBoard) -> str:
        """Return URL to this view."""
        return reverse(
            "workspace:workspace-boards:read-update-delete",
            args=(workspace_board.uuid,),
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

    def test_updating(
        self,
        rest_user_client: APIClient,
        resource_url: str,
        workspace_user: WorkspaceUser,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Test updating a ws board."""
        # TODO I hope there is no N+1 prob here, it used to be 12 queries
        # but with the addition of other_workspace_user as part of the fixture
        # it increased
        with django_assert_num_queries(13):
            response = rest_user_client.put(
                resource_url,
                data={
                    "title": "Project 1337",
                    "description": "This is Project 1337",
                    "deadline": now(),
                },
                format="json",
            )
            assert response.status_code == status.HTTP_200_OK, response.data

    def test_deleting(
        self,
        rest_user_client: APIClient,
        resource_url: str,
        workspace_user: WorkspaceUser,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Test updating a ws board."""
        # Another victim to non-determinism / N+1
        with django_assert_num_queries(13):
            response = rest_user_client.delete(
                resource_url,
            )
            assert (
                response.status_code == status.HTTP_204_NO_CONTENT
            ), response.data
