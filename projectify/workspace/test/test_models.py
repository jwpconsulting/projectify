# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2021, 2022, 2023 JWP Consulting GK
"""Test workspace models."""

from django import db
from django.core.exceptions import ValidationError

import psycopg.errors
import pytest

from ..models import ChatMessage, Label, SubTask, Task, TeamMember, Workspace
from ..services.sub_task import sub_task_create

pytestmark = pytest.mark.django_db


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


class TestLabel:
    """Test Label model."""

    def test_factory(self, label: Label) -> None:
        """Test factory."""
        assert label.color is not None


class TestSubTask:
    """Test SubTask."""

    def test_factory(self, task: Task, sub_task: SubTask) -> None:
        """Test that sub task correctly belongs to task."""
        assert sub_task.task == task

    def test_moving_sub_task(
        self, task: Task, sub_task: SubTask, team_member: TeamMember
    ) -> None:
        """Test moving a sub task around."""
        other_sub_task = sub_task_create(
            task=task,
            who=team_member.user,
            title="don't care",
            done=False,
        )
        other_other_sub_task = sub_task_create(
            task=task,
            who=team_member.user,
            title="don't care",
            done=False,
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
        self, task: Task, sub_task: SubTask
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


class TestChatMessage:
    """Test ChatMessage."""

    def test_factory(
        self, team_member: TeamMember, chat_message: ChatMessage
    ) -> None:
        """Test that chat message belongs to user."""
        assert chat_message.author == team_member


class TestTask:
    """Test Task."""

    def test_task_number(self, task: Task, other_task: Task) -> None:
        """Test unique task number."""
        other_task.refresh_from_db()
        task.refresh_from_db()
        assert other_task.number == task.number + 1
        task.workspace.refresh_from_db()
        assert task.workspace.highest_task_number == other_task.number

    def test_save(self, task: Task) -> None:
        """Test saving and assert number does not change."""
        num = task.number
        task.save()
        assert task.number == num

    def test_save_no_number(self, task: Task, workspace: Workspace) -> None:
        """Test saving with no number."""
        # With psycopg2 we had an db.InternalError, now with psycopg 3 it
        # became db.ProgrammingError instead
        with pytest.raises(db.ProgrammingError):
            task.number = None  # type: ignore[assignment]
            task.save()
            workspace.refresh_from_db()

    def test_save_different_number(self, task: Task) -> None:
        """Test saving with different number."""
        # Changed from db.InternalError, see above in test_save_no_number
        with pytest.raises(db.ProgrammingError):
            task.number = 154785787
            task.save()

    def test_task_workspace_pgtrigger(
        self, task: Task, unrelated_workspace: Workspace
    ) -> None:
        """Test database trigger for wrong workspace assignment."""
        # Changed from db.InternalError, see above in test_save_no_number
        with pytest.raises(db.ProgrammingError):
            task.workspace = unrelated_workspace
            task.save()
