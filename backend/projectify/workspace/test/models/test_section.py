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
"""Section model tests."""

import pytest

from ... import (
    models,
)


@pytest.mark.django_db
class TestSectionManager:
    """Test Section manager."""

    def test_filter_by_workspace_board_pks(
        self,
        workspace_board: models.WorkspaceBoard,
        section: models.Section,
    ) -> None:
        """Test filter_by_workspace_board_pks."""
        objects = models.Section.objects
        qs = objects.filter_by_workspace_board_pks(
            [workspace_board.pk],
        )
        assert list(qs) == [section]

    def test_filter_for_user_and_uuid(
        self,
        section: models.Section,
        workspace_user: models.WorkspaceUser,
        # TODO are these two fixtures needed?
        workspace: models.Workspace,
        other_workspace_user: models.WorkspaceUser,
    ) -> None:
        """Test getting for user and uuid."""
        actual = models.Section.objects.filter_for_user_and_uuid(
            workspace_user.user,
            section.uuid,
        ).get()
        assert actual == section


@pytest.mark.django_db
class TestSection:
    """Test Section."""

    def test_factory(
        self,
        workspace_board: models.WorkspaceBoard,
        section: models.Section,
    ) -> None:
        """Test section creation works."""
        assert section.workspace_board == workspace_board
