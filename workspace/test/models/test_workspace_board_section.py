# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Copyright (C) 2023 JWP Consulting GK
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
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
