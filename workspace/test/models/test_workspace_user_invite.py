"""Test WorkspaceUserInvite model."""

import pytest

from user.models import User
from workspace.models.workspace_user import WorkspaceUser

from ... import (
    models,
)
from ...exceptions import (
    UserAlreadyAdded,
    UserAlreadyInvited,
)
from ...models.workspace_user_invite import (
    add_or_invite_workspace_user,
)


@pytest.mark.django_db
class TestWorkspaceUserInviteQuerySet:
    """Test WorkspaceUserInviteQuerySet."""

    def test_filter_by_workspace_pks(
        self,
        workspace: models.Workspace,
        workspace_user_invite: models.WorkspaceUserInvite,
    ) -> None:
        """Test filter_by_workspace_pks."""
        qs = models.WorkspaceUserInvite.objects.filter_by_workspace_pks(
            [workspace.pk],
        )
        assert list(qs) == [workspace_user_invite]

    def test_filter_by_redeemed(
        self,
        workspace: models.Workspace,
        workspace_user_invite: models.WorkspaceUserInvite,
    ) -> None:
        """Test filter_by_redeemed."""
        qs = models.WorkspaceUserInvite.objects.filter_by_redeemed(False)
        assert qs.count() == 1
        workspace_user_invite.redeem()
        assert qs.count() == 0
        qs = models.WorkspaceUserInvite.objects.filter_by_redeemed(True)
        assert qs.count() == 1


@pytest.mark.django_db
class TestWorkspaceUserInvite:
    """Test workspace user invite."""

    def test_factory(
        self, workspace_user_invite: models.WorkspaceUserInvite
    ) -> None:
        """Test factory."""
        assert workspace_user_invite

    def test_redeem(
        self, workspace_user_invite: models.WorkspaceUserInvite
    ) -> None:
        """Test redeeming."""
        workspace_user_invite.redeem()
        workspace_user_invite.refresh_from_db()
        assert workspace_user_invite.redeemed

    def test_redeeming_twice(
        self, workspace_user_invite: models.WorkspaceUserInvite
    ) -> None:
        """Test redeeming twice."""
        workspace_user_invite.redeem()
        with pytest.raises(AssertionError):
            workspace_user_invite.redeem()

    def test_workspace(
        self,
        workspace_user_invite: models.WorkspaceUserInvite,
        workspace: models.Workspace,
    ) -> None:
        """Test workspace property."""
        assert workspace_user_invite.workspace == workspace


@pytest.mark.django_db
class TestAddOrInviteWorkspaceUser:
    """Test add_or_invite_workspace_user."""

    # We could probably use a more specific type for mailoutbox
    def test_invite_user(
        self,
        workspace: models.Workspace,
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
        self, workspace: models.Workspace, workspace_user: WorkspaceUser
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
        self, workspace: models.Workspace, workspace_user: models.WorkspaceUser
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
        workspace: models.Workspace,
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
        self, workspace_user: WorkspaceUser, workspace: models.Workspace
    ) -> None:
        """Test uninviting a user."""
        count = workspace.workspaceuserinvite_set.count()
        add_or_invite_workspace_user(
            who=workspace_user.user,
            workspace=workspace,
            email_or_user="hello@example.com",
        )
        assert workspace.workspaceuserinvite_set.count() == count + 1
        workspace.uninvite_user("hello@example.com")
        assert workspace.workspaceuserinvite_set.count() == count
