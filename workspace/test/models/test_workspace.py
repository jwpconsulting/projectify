"""Test Workspace model."""
from django import (
    db,
)
from django.contrib.auth.models import (
    AbstractUser,
)

import pytest

from workspace.exceptions import (
    UserAlreadyAdded,
    UserAlreadyInvited,
)
from workspace.models.workspace_user_invite import (
    add_or_invite_workspace_user,
)

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

    def test_add_workspace_board(self, workspace: models.Workspace) -> None:
        """Test adding a workspace board."""
        assert workspace.workspaceboard_set.count() == 0
        board = workspace.add_workspace_board("foo", "bar")
        assert workspace.workspaceboard_set.count() == 1
        board2 = workspace.add_workspace_board("foo", "bar")
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
        workspace.add_user(user)
        assert workspace.users.count() == 1

    def test_add_user_twice(
        self,
        workspace: models.Workspace,
        workspace_user: models.WorkspaceUser,
        user: AbstractUser,
    ) -> None:
        """Test that adding a user twice won't work."""
        with pytest.raises(db.IntegrityError):
            workspace.add_user(user)

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

    # TODO
    # We could probably use a more specific type for mailoutbox
    def test_invite_user(
        self, workspace: models.Workspace, mailoutbox: list[object]
    ) -> None:
        """Test inviting a user."""
        workspace_user_invite = add_or_invite_workspace_user(
            workspace, "hello@example.com"
        )
        assert workspace_user_invite.workspace == workspace
        assert len(mailoutbox) == 1

    def test_inviting_twice(self, workspace: models.Workspace) -> None:
        """Test that inviting twice won't work."""
        add_or_invite_workspace_user(workspace, "hello@example.com")
        with pytest.raises(UserAlreadyInvited):
            add_or_invite_workspace_user(workspace, "hello@example.com")

    def test_inviting_workspace_user(
        self, workspace: models.Workspace, workspace_user: models.WorkspaceUser
    ) -> None:
        """Test that inviting a pre-existing user won't work."""
        with pytest.raises(UserAlreadyAdded):
            add_or_invite_workspace_user(workspace, workspace_user.user.email)

    def test_inviting_user(
        self, workspace: models.Workspace, user: AbstractUser
    ) -> None:
        """Test that inviting an existing user will work."""
        assert workspace.workspaceuser_set.count() == 0
        add_or_invite_workspace_user(workspace, user.email)
        assert workspace.workspaceuser_set.count() == 1

    def test_uninviting_user(self, workspace: models.Workspace) -> None:
        """Test uninviting a user."""
        add_or_invite_workspace_user(workspace, "hello@example.com")
        assert workspace.workspaceuserinvite_set.count() == 1
        workspace.uninvite_user("hello@example.com")
        assert workspace.workspaceuserinvite_set.count() == 0

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
