"""Workspace board section model tests."""

import pytest

from ... import (
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
        workspace_board_section: models.WorkspaceBoardSection,
        workspace_user: models.WorkspaceUser,
        # TODO are these two fixtures needed?
        workspace: models.Workspace,
        other_workspace_user: models.WorkspaceUser,
    ) -> None:
        """Test getting for user and uuid."""
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

    def test_workspace(
        self,
        workspace: models.Workspace,
        workspace_board_section: models.WorkspaceBoardSection,
    ) -> None:
        """Test workspace property."""
        assert workspace_board_section.workspace == workspace
