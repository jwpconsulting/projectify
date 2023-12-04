"""Test workspace signals."""
from typing import (
    TYPE_CHECKING,
)

import pytest

from user.services.user import user_create
from workspace.models.workspace_user import WorkspaceUser
from workspace.services.workspace_user_invite import (
    add_or_invite_workspace_user,
    uninvite_user,
)

from .. import (
    models,
)

if TYPE_CHECKING:
    from user.models import User  # noqa: F401


@pytest.mark.django_db
class TestRedeemWorkspaceInvitations:
    """Test redeem_workspace_invitations."""

    def test_simple(
        self,
        workspace: models.Workspace,
        user_model: "User",
        workspace_user: WorkspaceUser,
    ) -> None:
        """Test simple case."""
        count = workspace.users.count()
        add_or_invite_workspace_user(
            who=workspace_user.user,
            workspace=workspace,
            email_or_user="hello@example.com",
        )
        assert workspace.users.count() == count
        user_create("hello@example.com")
        assert workspace.users.count() == count + 1

    def test_signs_up_twice(
        self,
        workspace: models.Workspace,
        user_model: "User",
        workspace_user: WorkspaceUser,
    ) -> None:
        """Test what happens if a user signs up twice."""
        count = workspace.users.count()
        add_or_invite_workspace_user(
            who=workspace_user.user,
            workspace=workspace,
            email_or_user="hello@example.com",
        )
        user = user_create("hello@example.com")
        assert workspace.users.count() == count + 1
        user.delete()
        assert workspace.users.count() == count
        user = user_create("hello@example.com")
        # The user is not automatically added
        assert workspace.users.count() == count

    def test_after_uninvite(
        self,
        workspace: models.Workspace,
        user_model: "User",
        workspace_user: WorkspaceUser,
    ) -> None:
        """Test what happens when a user is uninvited."""
        count = workspace.users.count()
        add_or_invite_workspace_user(
            who=workspace_user.user,
            workspace=workspace,
            email_or_user="hello@example.com",
        )
        assert workspace.users.count() == count
        uninvite_user(
            who=workspace_user.user,
            workspace=workspace,
            email="hello@example.com",
        )
        user_create("hello@example.com")
        # The user is not added
        assert workspace.users.count() == count
