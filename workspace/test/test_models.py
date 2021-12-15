"""Test workspace models."""
import pytest


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
