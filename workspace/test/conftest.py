"""Workspace test fixtures."""
import pytest

from .. import (
    factory,
)


@pytest.fixture
def workspace():
    """Return workspace."""
    return factory.WorkspaceFactory()


@pytest.fixture
def workspace_user(workspace, user):
    """Return workspace user."""
    return factory.WorkspaceUserFactory(workspace=workspace, user=user)


@pytest.fixture
def workspace_board(workspace):
    """Return workspace board."""
    return factory.WorkspaceBoardFactory(workspace=workspace)


@pytest.fixture
def workspace_board_section(workspace_board):
    """Return workspace board section."""
    return factory.WorkspaceBoardSectionFactory(
        workspace_board=workspace_board,
    )
