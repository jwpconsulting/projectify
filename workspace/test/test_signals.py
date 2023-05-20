"""Test workspace signals."""
import pytest


@pytest.mark.django_db
class TestRedeemWorkspaceInvitations:
    """Test redeem_workspace_invitations."""

    def test_simple(self, workspace, user_model):
        """Test simple case."""
        workspace.invite_user("hello@example.com")
        assert workspace.users.count() == 0
        user_model.objects.create_user("hello@example.com")
        assert workspace.users.count() == 1

    def test_signs_up_twice(self, workspace, user_model):
        """Test what happens if a user signs up twice."""
        workspace.invite_user("hello@example.com")
        user = user_model.objects.create_user("hello@example.com")
        assert workspace.users.count() == 1
        user.delete()
        assert workspace.users.count() == 0
        user = user_model.objects.create_user("hello@example.com")
        # The user is not automatically added
        assert workspace.users.count() == 0

    def test_after_uninvite(self, workspace, user_model):
        """Test what happens when a user is uninvited."""
        workspace.invite_user("hello@example.com")
        workspace.uninvite_user("hello@example.com")
        user_model.objects.create_user("hello@example.com")
        # The user is not added
        assert workspace.users.count() == 0
