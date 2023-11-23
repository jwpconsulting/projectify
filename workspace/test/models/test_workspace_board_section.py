"""Workspace board section model tests."""
from django.utils import (
    timezone,
)

import pytest

from ... import (
    factory,
    models,
)


@pytest.mark.django_db
class TestWorkspaceBoardSectionManager:
    """Test WorkspaceBoardSection manager."""

    def test_filter_by_workspace_board_pks(
        self,
        workspace_board: models.WorkspaceBoard,
        workspace_board_section: models.WorkspaceBoardSection,
    ) -> None:
        """Test filter_by_workspace_board_pks."""
        objects = models.WorkspaceBoardSection.objects
        qs = objects.filter_by_workspace_board_pks(
            [workspace_board.pk],
        )
        assert list(qs) == [workspace_board_section]

    def test_filter_for_user_and_uuid(
        self,
        workspace: models.Workspace,
        workspace_board_section: models.WorkspaceBoardSection,
        workspace_user: models.WorkspaceUser,
    ) -> None:
        """Test getting for user and uuid."""
        factory.WorkspaceUserFactory(
            workspace=workspace,
        )
        actual = models.WorkspaceBoardSection.objects.filter_for_user_and_uuid(
            workspace_user.user,
            workspace_board_section.uuid,
        ).get()
        assert actual == workspace_board_section


@pytest.mark.django_db
class TestWorkspaceBoardSection:
    """Test WorkspaceBoardSection."""

    def test_factory(
        self,
        workspace_board: models.WorkspaceBoard,
        workspace_board_section: models.WorkspaceBoardSection,
    ) -> None:
        """Test workspace board section creation works."""
        assert workspace_board_section.workspace_board == workspace_board

    def test_add_task(
        self, workspace_board_section: models.WorkspaceBoardSection
    ) -> None:
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

    def test_add_task_deadline(
        self, workspace_board_section: models.WorkspaceBoardSection
    ) -> None:
        """Test adding a task with a deadline."""
        task = workspace_board_section.add_task(
            title="foo",
            description="bar",
            deadline=timezone.now(),
        )
        assert task.deadline is not None

    def test_workspace(
        self,
        workspace: models.Workspace,
        workspace_board_section: models.WorkspaceBoardSection,
    ) -> None:
        """Test workspace property."""
        assert workspace_board_section.workspace == workspace
