"""Test workspace signals."""
from django.contrib import (
    auth,
)

import pytest


@pytest.mark.django_db
class TestRedeemWorkspaceInvitations:
    """Test redeem_workspace_invitations."""

    def test_simple(self, workspace):
        """Test simple case."""
        User = auth.get_user_model()
        workspace.invite_user("hello@example.com")
        assert workspace.users.count() == 0
        User.objects.create_user("hello@example.com")
        assert workspace.users.count() == 1

    def test_signs_up_twice(self, workspace):
        """Test what happens if a user signs up twice."""
        User = auth.get_user_model()
        workspace.invite_user("hello@example.com")
        user = User.objects.create_user("hello@example.com")
        assert workspace.users.count() == 1
        user.delete()
        assert workspace.users.count() == 0
        user = User.objects.create_user("hello@example.com")
        # The user is not automatically added
        assert workspace.users.count() == 0
