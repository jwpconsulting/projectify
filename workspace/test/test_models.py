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
        """Test getting workspaces for user."""
        workspace = workspace_user.workspace
        factory.WorkspaceFactory(add_users=[other_user])
        assert list(models.Workspace.objects.get_for_user(user)) == [workspace]

    def test_get_for_user_and_uuid(self, workspace_user, workspace, user):
        """Test getting workspace for user and uuid."""
        assert (
            models.Workspace.objects.get_for_user_and_uuid(
                user,
                workspace.uuid,
            )
            == workspace
        )


@pytest.mark.django_db
class TestWorkspace:
    """Test Workspace."""

    def test_factory(self, workspace):
        """Assert that the creates."""
        assert workspace

    def test_add_workspace_board(self, workspace):
        """Test adding a workspace board."""
        assert workspace.workspaceboard_set.count() == 0
        board = workspace.add_workspace_board("foo", "bar")
        assert workspace.workspaceboard_set.count() == 1
        board2 = workspace.add_workspace_board("foo", "bar")
        assert workspace.workspaceboard_set.count() == 2
        assert list(workspace.workspaceboard_set.all()) == [
            board,
            board2,
        ]


@pytest.mark.django_db
class TestWorkspaceUserManager:
    """Test workspace user manager."""

    def test_filter_by_workspace_pks(self, workspace_user, workspace):
        """Test filter_by_workspace_pks."""
        qs = models.WorkspaceUser.objects.filter_by_workspace_pks(
            [workspace.pk],
        )
        assert list(qs) == [workspace_user]


@pytest.mark.django_db
class TestWorkspaceUser:
    """Test WorkspaceUser."""

    def test_factory(self, workspace, workspace_user):
        """Test workspace user creation."""
        assert workspace_user.workspace == workspace


@pytest.mark.django_db
class TestWorkspaceBoardManager:
    """Test WorkspaceBoard manager."""

    def test_filter_by_workspace_pks(self, workspace, workspace_board):
        """Test filter_by_workspace_pks."""
        qs = models.WorkspaceBoard.objects.filter_by_workspace_pks(
            [workspace.pk],
        )
        assert list(qs) == [workspace_board]

    def test_get_for_user_and_uuid(
        self,
        workspace,
        workspace_board,
        workspace_user,
    ):
        """Test that the workspace board is retrieved correctly."""
        factory.WorkspaceUserFactory(
            workspace=workspace,
        )
        assert workspace_board.workspace.users.count() == 2
        actual = models.WorkspaceBoard.objects.get_for_user_and_uuid(
            workspace_user.user,
            workspace_board.uuid,
        )
        assert actual == workspace_board


@pytest.mark.django_db
class TestWorkspaceBoard:
    """Test WorkspaceBoard."""

    def test_factory(self, workspace, workspace_board):
        """Test workspace board creation works."""
        assert workspace_board.workspace == workspace

    def test_add_workspace_board_section(self, workspace_board):
        """Test workspace board section creation."""
        assert workspace_board.workspaceboardsection_set.count() == 0
        section = workspace_board.add_workspace_board_section(
            "hello",
            "world",
        )
        assert workspace_board.workspaceboardsection_set.count() == 1
        section2 = workspace_board.add_workspace_board_section(
            "hello",
            "world",
        )
        assert workspace_board.workspaceboardsection_set.count() == 2
        assert list(workspace_board.workspaceboardsection_set.all()) == [
            section,
            section2,
        ]


@pytest.mark.django_db
class TestWorkspaceBoardSectionManager:
    """Test WorkspaceBoardSection manager."""

    def test_filter_by_workspace_board_pks(
        self,
        workspace_board,
        workspace_board_section,
    ):
        """Test filter_by_workspace_board_pks."""
        objects = models.WorkspaceBoardSection.objects
        qs = objects.filter_by_workspace_board_pks(
            [workspace_board.pk],
        )
        assert list(qs) == [workspace_board_section]

    def test_get_for_user_and_uuid(
        self,
        workspace,
        workspace_board_section,
        workspace_user,
    ):
        """Test getting for user and uuid."""
        factory.WorkspaceUserFactory(
            workspace=workspace,
        )
        actual = models.WorkspaceBoardSection.objects.get_for_user_and_uuid(
            workspace_user.user,
            workspace_board_section.uuid,
        )
        assert actual == workspace_board_section


@pytest.mark.django_db
class TestWorkspaceBoardSection:
    """Test WorkspaceBoardSection."""

    def test_factory(self, workspace_board_section, workspace_board):
        """Test workspace board section creation works."""
        assert workspace_board_section.workspace_board == workspace_board

    def test_add_task(self, workspace_board_section):
        """Test adding tasks to a workspace board."""
        assert workspace_board_section.task_set.count() == 0
        task = workspace_board_section.add_task(title="foo", description="bar")
        assert workspace_board_section.task_set.count() == 1
        task2 = workspace_board_section.add_task(
            title="foo2",
            description="bar2",
        )
        assert workspace_board_section.task_set.count() == 2
        assert list(workspace_board_section.task_set.all()) == [task, task2]


@pytest.mark.django_db
class TestTaskManager:
    """Test TaskManager."""

    def test_filter_by_workspace_board_section_pks(
        self, workspace_board_section, task
    ):
        """Test filter_by_workspace_board_section_pks."""
        qs = models.Task.objects.filter_by_workspace_board_section_pks(
            [workspace_board_section.pk],
        )
        assert list(qs) == [task]

    def test_get_for_user_and_uuid(self, workspace, task, workspace_user):
        """Test get_for_user_and_uuid."""
        factory.WorkspaceUserFactory(
            workspace=workspace,
        )
        actual = models.Task.objects.get_for_user_and_uuid(
            workspace_user.user,
            task.uuid,
        )
        assert actual == task


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

    def test_add_sub_task(self, task):
        """Test adding a sub task."""
        assert task.subtask_set.count() == 0
        task.add_sub_task("foo", "bar")
        assert task.subtask_set.count() == 1


@pytest.mark.django_db
class TestSubTaskManager:
    """Test SubTask manager."""

    def test_filter_by_task_pks(self, task, sub_task):
        """Test filter_by_task_pks."""
        qs = models.SubTask.objects.filter_by_task_pks([task.pk])
        assert list(qs) == [sub_task]


@pytest.mark.django_db
class TestSubTask:
    """Test SubTask."""

    def test_factory(self, task, sub_task):
        """Test that sub task correctly belongs to task."""
        assert sub_task.task == task
