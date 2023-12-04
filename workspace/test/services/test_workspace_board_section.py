"""Test workspace board section services."""
import pytest
from rest_framework import serializers

from workspace.models import WorkspaceBoard
from workspace.models.task import Task
from workspace.models.workspace_board_section import WorkspaceBoardSection
from workspace.models.workspace_user import WorkspaceUser
from workspace.services.task import task_delete
from workspace.services.workspace_board_section import (
    workspace_board_section_delete,
    workspace_board_section_move,
)


@pytest.mark.django_db
def test_delete_non_empty_section(
    workspace_user: WorkspaceUser,
    workspace_board_section: WorkspaceBoardSection,
    # Make sure there is a task
    task: Task,
) -> None:
    """Assert we can't delete a non-empty section."""
    with pytest.raises(serializers.ValidationError) as error:
        workspace_board_section_delete(
            workspace_board_section=workspace_board_section,
            who=workspace_user.user,
        )
    assert error.match("still has tasks")

    # ... but if we delete the task,
    task_delete(
        task=task,
        who=workspace_user.user,
    )
    # it will work
    workspace_board_section_delete(
        workspace_board_section=workspace_board_section,
        who=workspace_user.user,
    )


@pytest.mark.django_db
def test_moving_section(
    workspace_board: WorkspaceBoard,
    workspace_board_section: WorkspaceBoardSection,
    other_workspace_board_section: WorkspaceBoardSection,
    other_other_workspace_board_section: WorkspaceBoardSection,
    workspace_user: WorkspaceUser,
) -> None:
    """Test moving a section around."""
    assert list(workspace_board.workspaceboardsection_set.all()) == [
        workspace_board_section,
        other_workspace_board_section,
        other_other_workspace_board_section,
    ]
    workspace_board_section_move(
        workspace_board_section=workspace_board_section,
        order=0,
        who=workspace_user.user,
    )
    assert list(workspace_board.workspaceboardsection_set.all()) == [
        workspace_board_section,
        other_workspace_board_section,
        other_other_workspace_board_section,
    ]
    workspace_board_section_move(
        workspace_board_section=workspace_board_section,
        order=2,
        who=workspace_user.user,
    )
    assert list(workspace_board.workspaceboardsection_set.all()) == [
        other_workspace_board_section,
        other_other_workspace_board_section,
        workspace_board_section,
    ]
    workspace_board_section_move(
        workspace_board_section=workspace_board_section,
        order=1,
        who=workspace_user.user,
    )
    assert list(workspace_board.workspaceboardsection_set.all()) == [
        other_workspace_board_section,
        workspace_board_section,
        other_other_workspace_board_section,
    ]


@pytest.mark.django_db
def test_moving_empty_section(
    workspace_board: WorkspaceBoard,
    workspace_board_section: WorkspaceBoardSection,
    workspace_user: WorkspaceUser,
) -> None:
    """Test moving when there are no other sections."""
    assert list(workspace_board.workspaceboardsection_set.all()) == [
        workspace_board_section,
    ]
    workspace_board_section_move(
        workspace_board_section=workspace_board_section,
        order=1,
        who=workspace_user.user,
    )
    assert list(workspace_board.workspaceboardsection_set.all()) == [
        workspace_board_section,
    ]
    assert workspace_board_section._order == 0
