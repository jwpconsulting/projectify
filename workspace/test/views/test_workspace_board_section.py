"""Test workspace board section CRUD views."""
from django.contrib.auth.models import (
    AbstractBaseUser,
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
)
from workspace.models import TaskLabel, WorkspaceBoard, WorkspaceBoardSection
from workspace.models.task import Task
from workspace.models.workspace import Workspace
from workspace.models.workspace_user import WorkspaceUser


# Create
@pytest.mark.django_db
class TestWorkspaceBoardSectionCreate:
    """Test workspace board section creation."""

    @pytest.fixture
    def resource_url(self) -> str:
        """Return URL to this view."""
        return reverse("workspace:workspace-board-sections:create")

    def test_authenticated(
        self,
        user: AbstractBaseUser,
        rest_user_client: APIClient,
        resource_url: str,
        django_assert_num_queries: DjangoAssertNumQueries,
        workspace_board: WorkspaceBoard,
        # Make sure that we are part of that workspace
        workspace_user: WorkspaceUser,
    ) -> None:
        """Assert that we can create a new workspace board."""
        assert WorkspaceBoardSection.objects.count() == 0
        with django_assert_num_queries(11):
            response = rest_user_client.post(
                resource_url,
                {
                    "title": "New workspace board section, who dis??",
                    "workspace_board_uuid": str(workspace_board.uuid),
                },
            )
        assert response.status_code == 201
        assert WorkspaceBoardSection.objects.count() == 1
        workspace_board_section = WorkspaceBoardSection.objects.get()
        assert (
            workspace_board_section.title
            == "New workspace board section, who dis??"
        )


# Read
@pytest.mark.django_db
class TestWorkspaceBoardSectionRead:
    """Test WorkspaceBoardSectionRetrieve view."""

    @pytest.fixture
    def resource_url(
        self, workspace_board_section: WorkspaceBoardSection
    ) -> str:
        """Return URL to this view."""
        return reverse(
            "workspace:workspace-board-sections:read-update",
            args=(workspace_board_section.uuid,),
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
        with django_assert_num_queries(6):
            response = rest_user_client.get(resource_url)
        assert response.status_code == 200, response.content

    def test_update(
        self,
        rest_user_client: APIClient,
        resource_url: str,
        user: AbstractBaseUser,
        workspace_user: WorkspaceUser,
        django_assert_num_queries: DjangoAssertNumQueries,
        workspace_board_section: WorkspaceBoardSection,
    ) -> None:
        """Test updating a workspace board section."""
        with django_assert_num_queries(10):
            response = rest_user_client.put(
                resource_url,
                data={
                    "title": "New title",
                    "description": "New description",
                },
            )
            assert response.status_code == status.HTTP_200_OK, response.data
        workspace_board_section.refresh_from_db()
        assert workspace_board_section.title == "New title"
        assert workspace_board_section.description == "New description"


# RPC
@pytest.mark.django_db
class TestWorkspaceBoardSectionMove:
    """Test moving a workspace board section."""

    @pytest.fixture
    def resource_url(
        self, workspace_board_section: WorkspaceBoardSection
    ) -> str:
        """Return URL to this view."""
        return reverse(
            "workspace:workspace-board-sections:move",
            args=(str(workspace_board_section.uuid),),
        )

    def test_authenticated_user(
        self,
        rest_user_client: APIClient,
        resource_url: str,
        django_assert_num_queries: DjangoAssertNumQueries,
        workspace_board_section: WorkspaceBoardSection,
        workspace_user: WorkspaceUser,
    ) -> None:
        """Test as an authenticated user."""
        other_workspace_board_section = WorkspaceBoardSection(
            workspace_board=workspace_board_section.workspace_board,
            title="test",
        )
        other_workspace_board_section.save()
        assert workspace_board_section._order == 0
        assert other_workspace_board_section._order == 1
        # XXX that's a whole lot of queries
        with django_assert_num_queries(24):
            response = rest_user_client.post(
                resource_url,
                data={
                    "order": 1,
                },
            )

        assert response.status_code == status.HTTP_200_OK, response.data
        workspace_board_section.refresh_from_db()
        other_workspace_board_section.refresh_from_db()
        assert other_workspace_board_section._order == 0
        assert workspace_board_section._order == 1
