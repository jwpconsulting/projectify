"""Test task services."""
from datetime import datetime

import pytest

from workspace.factory import TaskFactory, WorkspaceBoardSectionFactory
from workspace.models import WorkspaceBoard
from workspace.models.task import Task
from workspace.models.workspace_board_section import WorkspaceBoardSection
from workspace.models.workspace_user import WorkspaceUser
from workspace.services.task import task_create, task_move_after


# Create
@pytest.mark.django_db
def test_create_task(
    workspace_board_section: WorkspaceBoardSection,
    workspace_user: WorkspaceUser,
) -> None:
    """Test adding tasks to a workspace board."""
    assert workspace_board_section.task_set.count() == 0
    task = task_create(
        who=workspace_user.user,
        workspace_board_section=workspace_board_section,
        title="foo",
        description="bar",
    )
    assert workspace_board_section.task_set.count() == 1
    task2 = task_create(
        who=workspace_user.user,
        workspace_board_section=workspace_board_section,
        title="foo",
        description="bar",
    )
    assert workspace_board_section.task_set.count() == 2
    assert list(workspace_board_section.task_set.all()) == [task, task2]


@pytest.mark.django_db
def test_add_task_deadline(
    workspace_board_section: WorkspaceBoardSection,
    workspace_user: WorkspaceUser,
    now: datetime,
) -> None:
    """Test adding a task with a deadline."""
    task = task_create(
        workspace_board_section=workspace_board_section,
        who=workspace_user.user,
        title="foo",
        description="bar",
        deadline=now,
    )
    assert task.deadline is not None


@pytest.mark.django_db
def test_moving_task_within_section(
    workspace_board_section: WorkspaceBoardSection,
    task: Task,
    workspace_user: WorkspaceUser,
) -> None:
    """Test moving a task around within the same section."""
    other_task = TaskFactory.create(
        workspace_board_section=workspace_board_section
    )
    assert list(workspace_board_section.task_set.all()) == [
        task,
        other_task,
    ]
    task_move_after(
        who=workspace_user.user,
        task=task,
        workspace_board_section=workspace_board_section,
        after=other_task,
    )
    assert list(workspace_board_section.task_set.all()) == [
        other_task,
        task,
    ]


@pytest.mark.django_db
def test_moving_task_to_other_section(
    workspace_board: WorkspaceBoard,
    workspace_board_section: WorkspaceBoardSection,
    task: Task,
    workspace_user: WorkspaceUser,
) -> None:
    """Test moving a task around to another section."""
    other_task = TaskFactory.create(
        workspace_board_section=workspace_board_section
    )
    assert list(workspace_board_section.task_set.all()) == [
        task,
        other_task,
    ]
    other_section = WorkspaceBoardSectionFactory.create(
        workspace_board=workspace_board
    )
    other_section_task = TaskFactory.create(
        workspace_board_section=other_section,
    )
    assert list(other_section.task_set.all()) == [
        other_section_task,
    ]
    task_move_after(
        who=workspace_user.user,
        task=task,
        workspace_board_section=other_section,
        after=None,
    )
    assert list(other_section.task_set.all()) == [
        task,
        other_section_task,
    ]


@pytest.mark.django_db
def test_moving_task_to_empty_section(
    workspace_board: WorkspaceBoard,
    workspace_board_section: WorkspaceBoardSection,
    task: Task,
    workspace_user: WorkspaceUser,
) -> None:
    """
    Test what happens if we move it into an empty section.

    We also see what happens when the id is set too high.
    """
    other_section = WorkspaceBoardSectionFactory.create(
        workspace_board=workspace_board
    )
    task_move_after(
        who=workspace_user.user,
        task=task,
        workspace_board_section=other_section,
        after=None,
    )
    assert list(other_section.task_set.all()) == [
        task,
    ]
    task.refresh_from_db()
    assert task._order == 0
