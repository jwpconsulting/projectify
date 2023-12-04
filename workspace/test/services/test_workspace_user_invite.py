"""Test WorkspaceUserInvite services."""
import pytest
from rest_framework import serializers

from user.models import User
from workspace.models.workspace import Workspace
from workspace.models.workspace_user import WorkspaceUser
from workspace.services.workspace_user_invite import (
    add_or_invite_workspace_user,
    uninvite_user,
)

from ...exceptions import (
    UserAlreadyAdded,
    UserAlreadyInvited,
)


@pytest.mark.django_db
class TestAddOrInviteWorkspaceUser:
    """Test add_or_invite_workspace_user."""

    # We could probably use a more specific type for mailoutbox
    def test_invite_user(
        self,
        workspace: Workspace,
        mailoutbox: list[object],
        workspace_user: WorkspaceUser,
    ) -> None:
        """Test inviting a user."""
        workspace_user_invite = add_or_invite_workspace_user(
            who=workspace_user.user,
            workspace=workspace,
            email_or_user="hello@example.com",
        )
        assert workspace_user_invite.workspace == workspace
        assert len(mailoutbox) == 1

    def test_inviting_twice(
        self, workspace: Workspace, workspace_user: WorkspaceUser
    ) -> None:
        """Test that inviting twice won't work."""
        add_or_invite_workspace_user(
            who=workspace_user.user,
            workspace=workspace,
            email_or_user="hello@example.com",
        )
        with pytest.raises(UserAlreadyInvited):
            add_or_invite_workspace_user(
                who=workspace_user.user,
                workspace=workspace,
                email_or_user="hello@example.com",
            )

    def test_inviting_workspace_user(
        self, workspace: Workspace, workspace_user: WorkspaceUser
    ) -> None:
        """Test that inviting a pre-existing user won't work."""
        with pytest.raises(UserAlreadyAdded):
            add_or_invite_workspace_user(
                workspace=workspace,
                who=workspace_user.user,
                email_or_user=workspace_user.user.email,
            )

    def test_inviting_user(
        self,
        workspace: Workspace,
        unrelated_user: User,
        workspace_user: WorkspaceUser,
    ) -> None:
        """Test that inviting an existing user will work."""
        count = workspace.workspaceuser_set.count()
        add_or_invite_workspace_user(
            workspace=workspace,
            who=workspace_user.user,
            email_or_user=unrelated_user.email,
        )
        assert workspace.workspaceuser_set.count() == count + 1

    def test_uninviting_user(
        self, workspace_user: WorkspaceUser, workspace: Workspace
    ) -> None:
        """Test uninviting a user."""
        count = workspace.workspaceuserinvite_set.count()
        add_or_invite_workspace_user(
            who=workspace_user.user,
            workspace=workspace,
            email_or_user="hello@example.com",
        )
        assert workspace.workspaceuserinvite_set.count() == count + 1
        uninvite_user(
            workspace=workspace,
            who=workspace_user.user,
            email="hello@example.com",
        )
        assert workspace.workspaceuserinvite_set.count() == count

    def test_uninviting_user_on_no_invite(
        self, workspace_user: WorkspaceUser, workspace: Workspace
    ) -> None:
        """Test uninviting a user that was never invited."""
        count = workspace.workspaceuserinvite_set.count()
        with pytest.raises(serializers.ValidationError) as error:
            uninvite_user(
                workspace=workspace,
                who=workspace_user.user,
                email="hello@example.com",
            )
        assert error.match("was never invited")
        assert workspace.workspaceuserinvite_set.count() == count
