# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023-2024 JWP Consulting GK
"""Test Workspace model."""

from django import db
from django.core.exceptions import ValidationError

import psycopg.errors
import pytest

from projectify.user.models import User

from ...models import Task, TeamMember, Workspace
from ...services.project import project_create


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
