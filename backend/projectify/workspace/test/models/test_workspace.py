# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023-2024 JWP Consulting GK
"""Test Workspace model."""

from django import (
    db,
)
from django.core.exceptions import ValidationError

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

    def test_title_constraint(self, workspace: Workspace) -> None:
        """Assert we can not put URL-like strings in workspace.title."""
        # Copied from projectify/user/test/test_models.py and replaced
        # "user" -> "workspace", "preferred_name" -> "title"
        # Rejected
        workspace.title = "www.google.com"
        with pytest.raises(ValidationError):
            workspace.full_clean()

        workspace.title = "www.google.com."
        with pytest.raises(ValidationError):
            workspace.full_clean()

        workspace.title = "http://localhost"
        with pytest.raises(ValidationError):
            workspace.full_clean()

        # Can't be blank
        workspace.title = ""
        with pytest.raises(ValidationError):
            workspace.full_clean()

        # Allowed
        workspace.title = "John McHurDur Jr."
        workspace.full_clean()

        workspace.title = "http: //localhost"
        workspace.full_clean()

        workspace.title = "Department of: silly walks"
        workspace.full_clean()

        workspace.title = "www. google"
        workspace.full_clean()

        workspace.title = "Foob. Ar"
        workspace.full_clean()

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
        task.assignee = team_member
        task.save()
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
