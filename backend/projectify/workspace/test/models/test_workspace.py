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
"""Test Workspace model."""
from django import (
    db,
)
from django.contrib.auth.models import (
    AbstractUser,
)

import psycopg.errors
import pytest

from projectify.user.models import User
from projectify.workspace.models.const import WorkspaceUserRoles

from ...models.task import Task
from ...models.workspace import Workspace
from ...models.workspace_user import WorkspaceUser
from ...services.workspace import (
    workspace_add_user,
)
from ...services.workspace_board import (
    workspace_board_create,
)


@pytest.mark.django_db
class TestWorkspaceManager:
    """Test Workspace manager."""

    def test_get_for_user(
        self,
        user: AbstractUser,
        # This workplace shall be retrievable by the user
        workspace: Workspace,
        workspace_user: WorkspaceUser,
        # This workpace will not be retrieved since the user does not have a
        # workspace user for it
        unrelated_workspace_user: AbstractUser,
        unrelated_workspace: Workspace,
    ) -> None:
        """Test getting workspaces for user."""
        assert list(Workspace.objects.get_for_user(user)) == [workspace]

    def test_filter_for_user_and_uuid(
        self,
        workspace_user: WorkspaceUser,
        workspace: Workspace,
        user: AbstractUser,
    ) -> None:
        """Test getting workspace for user and uuid."""
        assert (
            Workspace.objects.filter_for_user_and_uuid(
                user,
                workspace.uuid,
            ).get()
            == workspace
        )


@pytest.mark.django_db
class TestWorkspace:
    """Test Workspace."""

    def test_factory(self, workspace: Workspace) -> None:
        """Assert that the creates."""
        assert workspace

    def test_add_workspace_board(
        self,
        workspace: Workspace,
        user: User,
        workspace_user: WorkspaceUser,
    ) -> None:
        """Test adding a workspace board."""
        assert workspace.workspaceboard_set.count() == 0
        board = workspace_board_create(
            workspace=workspace,
            title="foo",
            description="bar",
            who=user,
        )
        assert workspace.workspaceboard_set.count() == 1
        board2 = workspace_board_create(
            workspace=workspace,
            title="foo",
            description="bar",
            who=user,
        )
        assert workspace.workspaceboard_set.count() == 2
        # Workspace boards are ordered by most recently created
        assert list(workspace.workspaceboard_set.all()) == [
            board2,
            board,
        ]

    # TODO these tests should be in workspace service tests
    def test_add_user(self, workspace: Workspace, other_user: User) -> None:
        """Test adding a user."""
        count = workspace.users.count()
        workspace_add_user(
            workspace=workspace,
            user=other_user,
            role=WorkspaceUserRoles.OBSERVER,
        )
        assert workspace.users.count() == count + 1

    def test_add_user_twice(
        self,
        workspace: Workspace,
        workspace_user: WorkspaceUser,
        other_user: AbstractUser,
    ) -> None:
        """Test that adding a user twice won't work."""
        workspace_add_user(
            workspace=workspace,
            user=other_user,
            role=WorkspaceUserRoles.OBSERVER,
        )
        # XXX TODO should be validationerror, not integrityerror
        # We might get a bad 500 here, could be 400 instead
        with pytest.raises(db.IntegrityError):
            workspace_add_user(
                workspace=workspace,
                user=other_user,
                role=WorkspaceUserRoles.OBSERVER,
            )

    def test_remove_user(
        self,
        workspace: Workspace,
        workspace_user: WorkspaceUser,
        user: AbstractUser,
    ) -> None:
        """Test remove_user."""
        count = workspace.users.count()
        workspace.remove_user(user)
        assert workspace.users.count() == count - 1

    def test_remove_user_when_assigned(
        self,
        workspace: Workspace,
        task: Task,
        workspace_user: WorkspaceUser,
        user: AbstractUser,
    ) -> None:
        """Assert that the user is removed when removing the workspace user."""
        task.assign_to(workspace_user)
        task.refresh_from_db()
        assert task.assignee == workspace_user
        workspace.remove_user(user)
        task.refresh_from_db()
        assert task.assignee is None

    def test_increment_highest_task_number(self, workspace: Workspace) -> None:
        """Test set_highest_task_number."""
        num = workspace.highest_task_number
        new = workspace.increment_highest_task_number()
        assert new == num + 1
        workspace.refresh_from_db()
        assert workspace.highest_task_number == new

    def test_wrong_highest_task_number(
        self, workspace: Workspace, task: Task
    ) -> None:
        """Test db trigger when highest_task_number < highest child task."""
        # Changed from db.InternalError
        with pytest.raises(db.ProgrammingError) as e:
            task.save()
            workspace.highest_task_number = 0
            workspace.save()
        assert isinstance(e.value.__cause__, psycopg.errors.RaiseException)
