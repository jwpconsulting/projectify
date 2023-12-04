"""Test WorkspaceUserInvite model."""
import pytest

from ... import (
    models,
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
