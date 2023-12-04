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
from workspace.models import TaskLabel
from workspace.models.task import Task
from workspace.models.workspace import Workspace
from workspace.models.workspace_board import WorkspaceBoard
from workspace.models.workspace_user import WorkspaceUser
from workspace.selectors.workspace_board import (
    workspace_board_find_by_workspace_uuid,
)


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
        with django_assert_num_queries(7):
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

    def test_getting(
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
        # Make sure section -> task -> workspace_user -> user is resolved
        task.assignee = workspace_user
        task.save()
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
        with django_assert_num_queries(7):
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
        with django_assert_num_queries(8):
            response = rest_user_client.delete(
                resource_url,
            )
            assert (
                response.status_code == status.HTTP_204_NO_CONTENT
            ), response.data


# Read (list)
@pytest.mark.django_db
class TestWorkspaceBoardsArchivedList:
    """Test WorkspaceBoardsArchived list."""

    @pytest.fixture
    def resource_url(self, workspace: Workspace) -> str:
        """Return URL to this view."""
        return reverse(
            "workspace:workspaces:archived-workspace-boards",
            args=(workspace.uuid,),
        )

    def test_authenticated(
        self,
        rest_user_client: APIClient,
        resource_url: str,
        workspace_user: WorkspaceUser,
        # In total 2 workspace boards, but only one shall be returned
        workspace_board: WorkspaceBoard,
        archived_workspace_board: WorkspaceBoard,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Assert we can GET this view this while being logged in."""
        with django_assert_num_queries(2):
            response = rest_user_client.get(resource_url)
            assert response.status_code == 200, response.content
        assert len(response.data) == 1
        assert response.data[0]["uuid"] == str(archived_workspace_board.uuid)


# RPC
@pytest.mark.django_db
class TestWorkspaceBoardArchive:
    """Test workspace board archival."""

    @pytest.fixture
    def resource_url(self, workspace_board: WorkspaceBoard) -> str:
        """Return URL to this view."""
        return reverse(
            "workspace:workspace-boards:archive",
            args=(str(workspace_board.uuid),),
        )

    def test_archiving_and_unarchiving(
        self,
        rest_user_client: APIClient,
        resource_url: str,
        django_assert_num_queries: DjangoAssertNumQueries,
        workspace: Workspace,
        workspace_user: WorkspaceUser,
    ) -> None:
        """Test archiving a board and then unarchiving it."""
        count = len(
            workspace_board_find_by_workspace_uuid(
                who=workspace_user.user,
                workspace_uuid=workspace.uuid,
                archived=False,
            )
        )
        with django_assert_num_queries(10):
            response = rest_user_client.post(
                resource_url,
                data={"archived": True},
            )
            assert response.status_code == 200, response.data
        assert (
            count
            == len(
                workspace_board_find_by_workspace_uuid(
                    who=workspace_user.user,
                    workspace_uuid=workspace.uuid,
                    archived=False,
                )
            )
            + 1
        )
        with django_assert_num_queries(10):
            response = rest_user_client.post(
                resource_url,
                data={"archived": False},
            )
            assert response.status_code == 200, response.data
        assert count == len(
            workspace_board_find_by_workspace_uuid(
                who=workspace_user.user,
                workspace_uuid=workspace.uuid,
                archived=False,
            )
        )
