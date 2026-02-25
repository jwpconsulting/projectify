# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2021, 2022, 2023 JWP Consulting GK
"""Test workspace models."""

import pytest

from projectify.workspace.models.team_member import TeamMember
from projectify.workspace.services.sub_task import sub_task_create

from .. import models


# TODO extract into workspace/test/models/test_label.py
@pytest.mark.django_db
class TestLabel:
    """Test Label model."""

    def test_factory(self, label: models.Label) -> None:
        """Test factory."""
        assert label.color is not None


# TODO extract into workspace/test/models/test_sub_task.py
@pytest.mark.django_db
class TestSubTask:
    """Test SubTask."""

    def test_factory(
        self, task: models.Task, sub_task: models.SubTask
    ) -> None:
        """Test that sub task correctly belongs to task."""
        assert sub_task.task == task

    def test_moving_sub_task(
        self,
        task: models.Task,
        sub_task: models.SubTask,
        team_member: TeamMember,
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
        self,
        task: models.Task,
        sub_task: models.SubTask,
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


# TODO extract into workspace/test/models/test_chat_message.py
@pytest.mark.django_db
class TestChatMessage:
    """Test ChatMessage."""

    def test_factory(
        self,
        team_member: models.TeamMember,
        chat_message: models.ChatMessage,
    ) -> None:
        """Test that chat message belongs to user."""
        assert chat_message.author == team_member
