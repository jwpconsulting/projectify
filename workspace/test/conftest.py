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
def other_workspace_user(workspace, other_user):
    """Return workspace user for other_user."""
    return factory.WorkspaceUserFactory(workspace=workspace, user=other_user)


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


@pytest.fixture
def task(workspace_board_section, user):
    """Return task."""
    return factory.TaskFactory(
        workspace_board_section=workspace_board_section,
        assignee=user,
    )


@pytest.fixture
def other_task(workspace_board_section):
    """Return another task belonging to the same workspace board section."""
    return factory.TaskFactory(
        workspace_board_section=workspace_board_section,
    )


@pytest.fixture
def sub_task(task):
    """Return subtask."""
    return factory.SubTaskFactory(
        task=task,
    )


@pytest.fixture
def chat_message(task, workspace_user):
    """Return ChatMessage instance."""
    return factory.ChatMessageFactory(
        task=task,
        author=workspace_user.user,
    )
