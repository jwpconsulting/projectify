"""Test workspace models."""
import pytest

from workspace.models.workspace_user import WorkspaceUser
from workspace.services.workspace_board_section import (
    workspace_board_section_create,
)

from .. import (
    factory,
    models,
)


@pytest.mark.django_db
class TestWorkspaceBoardManager:
    """Test WorkspaceBoard manager."""

    def test_filter_by_workspace(
        self,
        workspace: models.Workspace,
        workspace_board: models.WorkspaceBoard,
    ) -> None:
        """Test filter_by_workspace_uuid."""
        qs = models.WorkspaceBoard.objects.filter_by_workspace(workspace)
        assert list(qs) == [workspace_board]

    def test_filter_by_user(
        self,
        workspace_board: models.WorkspaceBoard,
        workspace_user: models.WorkspaceUser,
    ) -> None:
        """Test filter_by_user."""
        qs = models.WorkspaceBoard.objects.filter_by_user(workspace_user.user)
        assert list(qs) == [workspace_board]

    def test_filter_by_workspace_pks(
        self,
        workspace: models.Workspace,
        workspace_board: models.WorkspaceBoard,
    ) -> None:
        """Test filter_by_workspace_pks."""
        qs = models.WorkspaceBoard.objects.filter_by_workspace_pks(
            [workspace.pk],
        )
        assert list(qs) == [workspace_board]

    def test_filter_for_user_and_uuid(
        self,
        workspace: models.Workspace,
        workspace_board: models.WorkspaceBoard,
        workspace_user: models.WorkspaceUser,
    ) -> None:
        """Test that the workspace board is retrieved correctly."""
        factory.WorkspaceUserFactory(
            workspace=workspace,
        )
        assert workspace_board.workspace.users.count() == 2
        actual = models.WorkspaceBoard.objects.filter_for_user_and_uuid(
            workspace_user.user,
            workspace_board.uuid,
        )
        assert actual.get() == workspace_board

    def test_filter_by_archived(
        self, workspace_board: models.WorkspaceBoard
    ) -> None:
        """Test filter_by_archived."""
        qs_archived = models.WorkspaceBoard.objects.filter_by_archived(True)
        qs_unarchived = models.WorkspaceBoard.objects.filter_by_archived(False)
        assert qs_archived.count() == 0
        assert qs_unarchived.count() == 1
        workspace_board.archive()
        assert qs_archived.count() == 1
        assert qs_unarchived.count() == 0
        workspace_board.unarchive()
        assert qs_archived.count() == 0
        assert qs_unarchived.count() == 1


@pytest.mark.django_db
class TestWorkspaceBoard:
    """Test WorkspaceBoard."""

    def test_factory(
        self,
        workspace: models.Workspace,
        workspace_board: models.WorkspaceBoard,
    ) -> None:
        """Test workspace board creation works."""
        assert workspace_board.workspace == workspace

    def test_add_workspace_board_section(
        self,
        workspace_board: models.WorkspaceBoard,
        workspace_user: WorkspaceUser,
    ) -> None:
        """Test workspace board section creation."""
        assert workspace_board.workspaceboardsection_set.count() == 0
        section = workspace_board_section_create(
            who=workspace_user.user,
            workspace_board=workspace_board,
            title="hello",
            description="world",
        )
        assert workspace_board.workspaceboardsection_set.count() == 1
        section2 = workspace_board_section_create(
            who=workspace_user.user,
            workspace_board=workspace_board,
            title="hello",
            description="world",
        )
        assert workspace_board.workspaceboardsection_set.count() == 2
        assert list(workspace_board.workspaceboardsection_set.all()) == [
            section,
            section2,
        ]

    def test_archive(self, workspace_board: models.WorkspaceBoard) -> None:
        """Test archive method."""
        assert workspace_board.archived is None
        workspace_board.archive()
        assert workspace_board.archived is not None

    def test_unarchive(self, workspace_board: models.WorkspaceBoard) -> None:
        """Test unarchive method."""
        assert workspace_board.archived is None
        workspace_board.archive()
        assert workspace_board.archived is not None
        workspace_board.unarchive()
        assert workspace_board.archived is None

    def test_workspace(
        self,
        workspace: models.Workspace,
        workspace_board: models.WorkspaceBoard,
    ) -> None:
        """Test workspace property."""
        assert workspace_board.workspace == workspace


@pytest.mark.django_db
class TestLabelManager:
    """Test Label queryset/manager."""

    def test_filter_by_workspace_pks(
        self, label: models.Label, workspace: models.Workspace
    ) -> None:
        """Test filter_by_workspace_pks."""
        qs = models.Label.objects.filter_by_workspace_pks([workspace.pk])
        labels = [label]
        assert list(qs) == labels

    def test_filter_for_user_and_uuid(
        self, label: models.Label, workspace_user: models.WorkspaceUser
    ) -> None:
        """Test filter_for_user_and_uuid."""
        assert (
            models.Label.objects.filter_for_user_and_uuid(
                workspace_user.user,
                label.uuid,
            ).get()
            == label
        )


@pytest.mark.django_db
class TestLabel:
    """Test Label model."""

    def test_factory(self, label: models.Label) -> None:
        """Test factory."""
        assert label.color is not None

    def test_workspace(
        self, workspace: models.Workspace, label: models.Label
    ) -> None:
        """Test workspace property."""
        assert label.workspace == workspace


@pytest.mark.django_db
class TestLabelQuerySet:
    """Test LabelQuerySet."""

    def test_filter_by_task_pks(
        self, label: models.Label, task: models.Task
    ) -> None:
        """Test filter_by_task_pks."""
        task_label = task.add_label(label)
        qs = models.TaskLabel.objects.filter_by_task_pks([task.pk])
        task_labels = [task_label]
        assert list(qs) == task_labels


@pytest.mark.django_db
class TestTaskLabel:
    """Test TaskLabel model."""

    def test_factory(
        self,
        task_label: models.TaskLabel,
        task: models.Task,
        label: models.Label,
    ) -> None:
        """Test factory."""
        assert task_label.task == task
        assert task_label.label == label

    def test_workspace(
        self, workspace: models.Workspace, task_label: models.TaskLabel
    ) -> None:
        """Test workspace property."""
        assert task_label.workspace == workspace


@pytest.mark.django_db
class TestSubTaskManager:
    """Test SubTask manager."""

    def test_filter_by_task_pks(
        self, task: models.Task, sub_task: models.SubTask
    ) -> None:
        """Test filter_by_task_pks."""
        qs = models.SubTask.objects.filter_by_task_pks([task.pk])
        assert list(qs) == [sub_task]

    def test_filter_for_user_and_uuid(
        self, sub_task: models.SubTask, workspace_user: models.WorkspaceUser
    ) -> None:
        """Test filter_for_user_and_uuid."""
        assert (
            models.SubTask.objects.filter_for_user_and_uuid(
                workspace_user.user,
                sub_task.uuid,
            ).get()
            == sub_task
        )


@pytest.mark.django_db
class TestSubTask:
    """Test SubTask."""

    def test_factory(
        self, task: models.Task, sub_task: models.SubTask
    ) -> None:
        """Test that sub task correctly belongs to task."""
        assert sub_task.task == task

    def test_moving_sub_task(
        self, task: models.Task, sub_task: models.SubTask
    ) -> None:
        """Test moving a sub task around."""
        other_sub_task = factory.SubTaskFactory.create(
            task=task,
        )
        other_other_sub_task = factory.SubTaskFactory.create(
            task=task,
        )
        assert list(task.subtask_set.all()) == [
            sub_task,
            other_sub_task,
            other_other_sub_task,
        ]
        sub_task.move_to(0)
        assert list(task.subtask_set.all()) == [
            sub_task,
            other_sub_task,
            other_other_sub_task,
        ]
        sub_task.move_to(2)
        assert list(task.subtask_set.all()) == [
            other_sub_task,
            other_other_sub_task,
            sub_task,
        ]
        sub_task.move_to(1)
        assert list(task.subtask_set.all()) == [
            other_sub_task,
            sub_task,
            other_other_sub_task,
        ]

    def test_moving_within_empty_task(
        self,
        task: models.Task,
        sub_task: models.SubTask,
    ) -> None:
        """Test moving when there are no other sub tasks."""
        assert list(task.subtask_set.all()) == [
            sub_task,
        ]
        sub_task.move_to(1)
        assert list(task.subtask_set.all()) == [
            sub_task,
        ]
        assert sub_task._order == 0

    def test_workspace(
        self, workspace: models.Workspace, sub_task: models.SubTask
    ) -> None:
        """Test workspace property."""
        assert sub_task.workspace == workspace


@pytest.mark.django_db
class TestChatMessageManager:
    """Test ChatMessage Manager."""

    def test_filter_by_task_pks(
        self, chat_message: models.ChatMessage, task: models.Task
    ) -> None:
        """Test filter_by_task_pks."""
        qs = models.ChatMessage.objects.filter_by_task_pks([task.pk])
        assert list(qs) == [chat_message]

    def test_filter_for_user_and_uuid(
        self,
        chat_message: models.ChatMessage,
        workspace_user: models.WorkspaceUser,
    ) -> None:
        """Test filter_for_user_and_uuid."""
        assert (
            models.ChatMessage.objects.filter_for_user_and_uuid(
                workspace_user.user,
                chat_message.uuid,
            ).get()
            == chat_message
        )


@pytest.mark.django_db
class TestChatMessage:
    """Test ChatMessage."""

    def test_factory(
        self,
        workspace_user: models.WorkspaceUser,
        chat_message: models.ChatMessage,
    ) -> None:
        """Test that chat message belongs to user."""
        assert chat_message.author == workspace_user

    def test_workspace(
        self, workspace: models.Workspace, chat_message: models.ChatMessage
    ) -> None:
        """Test workspace property."""
        assert chat_message.workspace == workspace
