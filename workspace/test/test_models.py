"""Test workspace models."""
import pytest

from ..factory import (
    WorkspaceFactory,
)
from ..models import (
    Workspace,
)


@pytest.mark.django_db
class TestWorkspaceManager:
    """Test Workspace manager."""

    def test_get_for_user(self, workspace_user, user, other_user):
        """."""
        workspace = workspace_user.workspace
        WorkspaceFactory(add_users=[other_user])
        assert list(Workspace.objects.get_for_user(user)) == [workspace]


@pytest.mark.django_db
class TestWorkspace:
    """Test Workspace."""

    def test_factory(self, workspace):
        """Assert that the creates."""
        assert workspace


@pytest.mark.django_db
class TestWorkspaceUser:
    """Test WorkspaceUser."""

    def test_factory(self, workspace, workspace_user):
        """Test workspace user creation."""
        assert workspace_user.workspace == workspace


@pytest.mark.django_db
class TestWorkspaceBoard:
    """Test WorkspaceBoard."""

    def test_factory(self, workspace, workspace_board):
        """Test workspace board creation works."""
        assert workspace_board.workspace == workspace


@pytest.mark.django_db
class TestWorkspaceBoardSection:
    """Test WorkspaceBoardSection."""

    def test_factory(self, workspace_board_section, workspace_board):
        """Test workspace board section creation works."""
        assert workspace_board_section.workspace_board == workspace_board
