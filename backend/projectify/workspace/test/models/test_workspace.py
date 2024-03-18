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

import psycopg.errors
import pytest

from projectify.user.models import User
from projectify.workspace.models.const import TeamMemberRoles

from ...models.task import Task
from ...models.team_member import TeamMember
from ...models.workspace import Workspace
from ...services.project import project_create
from ...services.workspace import workspace_add_user


@pytest.mark.django_db
class TestWorkspace:
    """Test Workspace."""

    def test_factory(self, workspace: Workspace) -> None:
        """Assert that the creates."""
        assert workspace

    def test_add_project(
        self,
        workspace: Workspace,
        user: User,
        team_member: TeamMember,
    ) -> None:
        """Test adding a project."""
        assert workspace.project_set.count() == 0
        board = project_create(
            workspace=workspace,
            title="foo",
            description="bar",
            who=user,
        )
        assert workspace.project_set.count() == 1
        board2 = project_create(
            workspace=workspace,
            title="foo",
            description="bar",
            who=user,
        )
        assert workspace.project_set.count() == 2
        # Projects are ordered by most recently created
        assert list(workspace.project_set.all()) == [
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
            role=TeamMemberRoles.OBSERVER,
        )
        assert workspace.users.count() == count + 1

    def test_add_user_twice(
        self,
        workspace: Workspace,
        team_member: TeamMember,
        other_user: User,
    ) -> None:
        """Test that adding a user twice won't work."""
        workspace_add_user(
            workspace=workspace,
            user=other_user,
            role=TeamMemberRoles.OBSERVER,
        )
        # XXX TODO should be validationerror, not integrityerror
        # We might get a bad 500 here, could be 400 instead
        with pytest.raises(db.IntegrityError):
            workspace_add_user(
                workspace=workspace,
                user=other_user,
                role=TeamMemberRoles.OBSERVER,
            )

    def test_remove_user(
        self,
        workspace: Workspace,
        team_member: TeamMember,
        user: User,
    ) -> None:
        """Test remove_user."""
        count = workspace.users.count()
        workspace.remove_user(user)
        assert workspace.users.count() == count - 1

    def test_remove_user_when_assigned(
        self,
        workspace: Workspace,
        task: Task,
        team_member: TeamMember,
        user: User,
    ) -> None:
        """Assert that the user is removed when removing the team member."""
        task.assign_to(team_member)
        task.refresh_from_db()
        assert task.assignee == team_member
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
