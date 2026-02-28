# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2021, 2022, 2023 JWP Consulting GK
"""Test workspace models."""

import pytest

from ..models import ChatMessage, Label, SubTask, Task, TeamMember
from ..services.sub_task import sub_task_create


@pytest.mark.django_db
class TestLabel:
    """Test Label model."""

    def test_factory(self, label: Label) -> None:
        """Test factory."""
        assert label.color is not None


@pytest.mark.django_db
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


@pytest.mark.django_db
class TestChatMessage:
    """Test ChatMessage."""

    def test_factory(
        self, team_member: TeamMember, chat_message: ChatMessage
    ) -> None:
        """Test that chat message belongs to user."""
        assert chat_message.author == team_member
