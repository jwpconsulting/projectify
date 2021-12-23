"""Test workspace models."""
import pytest

from .. import (
    factory,
    models,
)


@pytest.mark.django_db
class TestWorkspaceManager:
    """Test Workspace manager."""

    def test_get_for_user(self, workspace_user, user, other_user):
        """."""
        workspace = workspace_user.workspace
        factory.WorkspaceFactory(add_users=[other_user])
        assert list(models.Workspace.objects.get_for_user(user)) == [workspace]


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


@pytest.mark.django_db
class TestTask:
    """Test Task."""

    def test_factory(self, workspace_board_section, task):
        """Test that workspace_board_section is assigned correctly."""
        assert task.workspace_board_section == workspace_board_section

    def test_moving_task_within_section(
        self,
        workspace_board_section,
        task,
    ):
        """Test moving a task around within the same section."""
        other_task = factory.TaskFactory(
            workspace_board_section=workspace_board_section
        )
        assert list(workspace_board_section.task_set.all()) == [
            task,
            other_task,
        ]
        task.move_to(workspace_board_section, 1)
        assert list(workspace_board_section.task_set.all()) == [
            other_task,
            task,
        ]

    def test_moving_task_to_other_section(
        self, workspace_board, workspace_board_section, task
    ):
        """Test moving a task around to another section."""
        other_task = factory.TaskFactory(
            workspace_board_section=workspace_board_section
        )
        assert list(workspace_board_section.task_set.all()) == [
            task,
            other_task,
        ]
        other_section = factory.WorkspaceBoardSectionFactory(
            workspace_board=workspace_board
        )
        other_section_task = factory.TaskFactory(
            workspace_board_section=other_section,
        )
        assert list(other_section.task_set.all()) == [
            other_section_task,
        ]
        task.move_to(other_section, 0)
        assert list(other_section.task_set.all()) == [
            task,
            other_section_task,
        ]

    def test_moving_task_to_empty_section(
        self, workspace_board, workspace_board_section, task
    ):
        """
        Test what happens if we move it into an empty section.

        We also see what happens when the id is set too high.
        """
        other_section = factory.WorkspaceBoardSectionFactory(
            workspace_board=workspace_board
        )
        task.move_to(other_section, 1)
        assert list(other_section.task_set.all()) == [
            task,
        ]
        task.refresh_from_db()
        assert task.order == 0


@pytest.mark.django_db
class TestSubTask:
    """Test SubTask."""

    def test_factory(self, task, sub_task):
        """Test that sub task correctly belongs to task."""
        assert sub_task.task == task
