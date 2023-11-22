"""Test Workspace model."""
from django import (
    db,
)
from django.contrib.auth.models import (
    AbstractUser,
)

import pytest

from user.models import User
from workspace.models.workspace_user import WorkspaceUser
from workspace.services.workspace import (
    workspace_add_user,
)
from workspace.services.workspace_board import workspace_board_create

from ... import (
    factory,
    models,
)


@pytest.mark.django_db
class TestWorkspaceManager:
    """Test Workspace manager."""

    def test_get_for_user(
        self,
        workspace_user: models.WorkspaceUser,
        user: AbstractUser,
        other_user: AbstractUser,
    ) -> None:
        """Test getting workspaces for user."""
        workspace = workspace_user.workspace
        factory.WorkspaceFactory(add_users=[other_user])
        assert list(models.Workspace.objects.get_for_user(user)) == [workspace]

    def test_filter_for_user_and_uuid(
        self,
        workspace_user: models.WorkspaceUser,
        workspace: models.Workspace,
        user: AbstractUser,
    ) -> None:
        """Test getting workspace for user and uuid."""
        assert (
            models.Workspace.objects.filter_for_user_and_uuid(
                user,
                workspace.uuid,
            ).get()
            == workspace
        )


@pytest.mark.django_db
class TestWorkspace:
    """Test Workspace."""

    def test_factory(self, workspace: models.Workspace) -> None:
        """Assert that the creates."""
        assert workspace

    def test_add_workspace_board(
        self,
        workspace: models.Workspace,
        user: User,
        workspace_user: WorkspaceUser,
    ) -> None:
        """Test adding a workspace board."""
        assert workspace.workspaceboard_set.count() == 0
        board = workspace_board_create(
            workspace=workspace,
            title="foo",
            description="bar",
            who=user,
        )
        assert workspace.workspaceboard_set.count() == 1
        board2 = workspace_board_create(
            workspace=workspace,
            title="foo",
            description="bar",
            who=user,
        )
        assert workspace.workspaceboard_set.count() == 2
        assert list(workspace.workspaceboard_set.all()) == [
            board,
            board2,
        ]

    def test_add_user(
        self, workspace: models.Workspace, user: AbstractUser
    ) -> None:
        """Test adding a user."""
        assert workspace.users.count() == 0
        workspace_add_user(workspace, user)
        assert workspace.users.count() == 1

    def test_add_user_twice(
        self,
        workspace: models.Workspace,
        workspace_user: models.WorkspaceUser,
        user: AbstractUser,
    ) -> None:
        """Test that adding a user twice won't work."""
        with pytest.raises(db.IntegrityError):
            workspace_add_user(workspace, user)

    def test_remove_user(
        self,
        workspace: models.Workspace,
        workspace_user: models.WorkspaceUser,
        user: AbstractUser,
    ) -> None:
        """Test remove_user."""
        assert workspace.users.count() == 1
        workspace.remove_user(user)
        assert workspace.users.count() == 0

    def test_remove_user_when_assigned(
        self,
        workspace: models.Workspace,
        task: models.Task,
        workspace_user: models.WorkspaceUser,
        user: AbstractUser,
    ) -> None:
        """Assert that the user is removed when removing the workspace user."""
        task.assign_to(workspace_user)
        task.refresh_from_db()
        assert task.assignee == workspace_user
        workspace.remove_user(user)
        task.refresh_from_db()
        assert task.assignee is None

    def test_increment_highest_task_number(
        self, workspace: models.Workspace
    ) -> None:
        """Test set_highest_task_number."""
        num = workspace.highest_task_number
        new = workspace.increment_highest_task_number()
        assert new == num + 1
        workspace.refresh_from_db()
        assert workspace.highest_task_number == new

    def test_wrong_highest_task_number(
        self, workspace: models.Workspace, task: models.Task
    ) -> None:
        """Test db trigger when highest_task_number < highest child task."""
        with pytest.raises(db.InternalError):
            task.save()
            workspace.highest_task_number = 0
            workspace.save()

    def test_has_at_least_role(
        self, workspace: models.Workspace, workspace_user: models.WorkspaceUser
    ) -> None:
        """Test has_at_least_role."""
        assert workspace.has_at_least_role(
            workspace_user,
            models.WorkspaceUserRoles.OWNER,
        )
        workspace_user.assign_role(models.WorkspaceUserRoles.OBSERVER)
        assert workspace.has_at_least_role(
            workspace_user,
            models.WorkspaceUserRoles.OBSERVER,
        )
        assert not workspace.has_at_least_role(
            workspace_user,
            models.WorkspaceUserRoles.OWNER,
        )

    def test_has_at_least_role_other_workspace(
        self,
        other_workspace: models.Workspace,
        workspace_user: models.WorkspaceUser,
    ) -> None:
        """Test has_at_least_role with a different workspace."""
        assert not other_workspace.has_at_least_role(
            workspace_user,
            models.WorkspaceUserRoles.OBSERVER,
        )

    def test_workspace(self, workspace: models.Workspace) -> None:
        """Test workspace property."""
        assert workspace.workspace == workspace
