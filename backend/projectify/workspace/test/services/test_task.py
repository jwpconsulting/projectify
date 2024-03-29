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
"""Test task services."""
from datetime import datetime

import pytest

from projectify.workspace.models import Project
from projectify.workspace.models.label import Label
from projectify.workspace.models.section import (
    Section,
)
from projectify.workspace.models.sub_task import SubTask
from projectify.workspace.models.task import Task
from projectify.workspace.models.team_member import TeamMember
from projectify.workspace.services.task import (
    task_create,
    task_create_nested,
    task_move_after,
    task_update_nested,
)

pytestmark = pytest.mark.django_db


# Create
def test_create_task(
    section: Section,
    team_member: TeamMember,
) -> None:
    """Test adding tasks to a project."""
    assert section.task_set.count() == 0
    task = task_create(
        who=team_member.user,
        section=section,
        title="foo",
        description="bar",
    )
    assert section.task_set.count() == 1
    task2 = task_create(
        who=team_member.user,
        section=section,
        title="foo",
        description="bar",
    )
    assert section.task_set.count() == 2
    assert list(section.task_set.all()) == [task, task2]


def test_task_create_nested(
    label: Label,
    team_member: TeamMember,
    section: Section,
) -> None:
    """Test task_create_nested."""
    task = task_create_nested(
        who=team_member.user,
        section=section,
        title="hello",
        description=None,
        assignee=team_member,
        due_date=None,
        labels=[label],
        sub_tasks={"create_sub_tasks": [], "update_sub_tasks": []},
    )
    assert list(task.labels.values_list("uuid", flat=True)) == [label.uuid]
    assert task.assignee == team_member


def test_add_task_due_date(
    section: Section,
    team_member: TeamMember,
    now: datetime,
) -> None:
    """Test adding a task with a due date."""
    task = task_create(
        section=section,
        who=team_member.user,
        title="foo",
        description="bar",
        due_date=now,
    )
    assert task.due_date is not None


# Update
def test_task_update_nested(
    task: Task,
    label: Label,
    team_member: TeamMember,
    other_team_member: TeamMember,
    sub_task: SubTask,
) -> None:
    """Test updating a task."""
    assert task.subtask_set.count() == 1
    task_update_nested(
        who=team_member.user,
        task=task,
        title="Hello world",
        description=None,
        assignee=other_team_member,
        labels=[label],
        sub_tasks={
            "create_sub_tasks": [
                {
                    "title": "Frobnice fluffballs",
                    "done": True,
                    "_order": 0,
                },
                {
                    "title": "Frebnecize flerfbowls",
                    "done": True,
                    "_order": 2,
                },
            ],
            "update_sub_tasks": [
                {
                    "uuid": sub_task.uuid,
                    "title": "Settle Catan",
                    "done": not sub_task.done,
                    "_order": 1,
                },
            ],
        },
    )
    task.refresh_from_db()
    assert task.assignee == other_team_member

    assert task.due_date is None

    assert list(task.labels.values_list("uuid", flat=True)) == [label.uuid]

    assert task.assignee
    assert task.assignee.user.email == other_team_member.user.email

    sub_tasks = list(task.subtask_set.all())
    assert len(sub_tasks) == 3
    assert sub_tasks[1].uuid == sub_task.uuid
    assert sub_tasks[1].done == (not sub_task.done)


def test_moving_task_within_section(
    section: Section,
    task: Task,
    team_member: TeamMember,
) -> None:
    """Test moving a task around within the same section."""
    other_task = task_create(
        who=team_member.user,
        title="don't care",
        section=section,
    )
    assert list(section.task_set.all()) == [
        task,
        other_task,
    ]
    task_move_after(
        who=team_member.user,
        task=task,
        after=other_task,
    )
    assert list(section.task_set.all()) == [
        other_task,
        task,
    ]


def test_moving_task_to_other_section(
    # TODO this fixture might not be needed
    project: Project,
    section: Section,
    other_section: Section,
    task: Task,
    team_member: TeamMember,
) -> None:
    """Test moving a task around to another section."""
    other_task = task_create(
        who=team_member.user,
        title="don't care",
        section=section,
    )
    assert list(section.task_set.all()) == [
        task,
        other_task,
    ]
    other_section_task = task_create(
        who=team_member.user,
        title="don't care",
        section=other_section,
    )
    assert list(other_section.task_set.all()) == [
        other_section_task,
    ]
    task_move_after(
        who=team_member.user,
        task=task,
        after=other_section,
    )
    assert list(other_section.task_set.all()) == [
        task,
        other_section_task,
    ]


def test_moving_task_to_empty_section(
    # TODO the following two fixtures might not be needed
    project: Project,
    section: Section,
    other_section: Section,
    task: Task,
    team_member: TeamMember,
) -> None:
    """
    Test what happens if we move it into an empty section.

    We also see what happens when the id is set too high.
    """
    task_move_after(
        who=team_member.user,
        task=task,
        after=other_section,
    )
    assert list(other_section.task_set.all()) == [
        task,
    ]
    task.refresh_from_db()
    assert task._order == 0
