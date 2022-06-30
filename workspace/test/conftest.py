"""Workspace test fixtures."""
import pytest

from corporate.factory import (
    CustomerFactory,
)

from .. import (
    factory,
    models,
)


@pytest.fixture
def workspace():
    """Return workspace."""
    workspace = factory.WorkspaceFactory()
    CustomerFactory(workspace=workspace)
    return workspace


@pytest.fixture
def other_workspace():
    """Return workspace."""
    return factory.WorkspaceFactory()


@pytest.fixture
def workspace_user_invite(workspace, user_invite):
    """Return workspace user invite."""
    return factory.WorkspaceUserInviteFactory(
        user_invite=user_invite,
        workspace=workspace,
    )


@pytest.fixture
def workspace_user(workspace, user):
    """Return workspace user with owner status."""
    return factory.WorkspaceUserFactory(
        workspace=workspace,
        user=user,
        role=models.WorkspaceUserRoles.OWNER,
    )


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
def task(workspace_board_section, workspace_user):
    """Return task."""
    return factory.TaskFactory(
        workspace_board_section=workspace_board_section,
        assignee=workspace_user,
    )


@pytest.fixture
def other_task(workspace_board_section):
    """Return another task belonging to the same workspace board section."""
    return factory.TaskFactory(
        workspace_board_section=workspace_board_section,
    )


@pytest.fixture
def label(workspace):
    """Return a label."""
    return factory.LabelFactory(
        workspace=workspace,
    )


@pytest.fixture
def task_label(task, label):
    """Return a label."""
    return factory.TaskLabelFactory(
        task=task,
        label=label,
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
        author=workspace_user,
    )
