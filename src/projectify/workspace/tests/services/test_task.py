# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023 JWP Consulting GK
"""Test task services."""

from datetime import datetime

from django.forms import ValidationError

import pytest

from ...models import Project, Task, TeamMember
from ...services.task import task_create, task_mark_done, task_update

pytestmark = pytest.mark.django_db


# Create
def test_create_task(
    project: Project, team_member: TeamMember, other_team_member: TeamMember
) -> None:
    """Test adding tasks to a project."""
    count = project.task_set.count()
    task = task_create(
        who=team_member.user, project=project, title_description="foo"
    )
    assert task.title == "foo"
    assert task.description == "foo"

    assert project.task_set.count() == count + 1

    task2 = task_create(
        who=team_member.user,
        project=project,
        title_description="<p>foo</p><p>bar</p>",
        assignee=other_team_member,
    )
    assert task2.title == "foo"
    assert task2.description == "<p>foo</p><p>bar</p>"

    assert project.task_set.count() == count + 2
    assert list(project.task_set.all()) == [task2, task]


def test_create_task_unrelated_teammember(
    project: Project,
    team_member: TeamMember,
    unrelated_team_member: TeamMember,
) -> None:
    """Test adding tasks to a project."""
    with pytest.raises(ValidationError) as e:
        task_create(
            who=team_member.user,
            project=project,
            title_description="foo",
            assignee=unrelated_team_member,
        )
    assert e.match("belongs to a different workspace")


def test_task_create_nested(team_member: TeamMember, project: Project) -> None:
    """Test task_create_nested."""
    task = task_create(
        who=team_member.user,
        project=project,
        title_description="foo",
        assignee=team_member,
    )
    assert task.assignee == team_member


def test_add_task_due_date(
    project: Project, team_member: TeamMember, now: datetime
) -> None:
    """Test adding a task with a due date."""
    task = task_create(
        project=project,
        who=team_member.user,
        title_description="foo",
        due_date=now,
    )
    assert task.due_date is not None


# Update
def test_task_update(
    task: Task, team_member: TeamMember, other_team_member: TeamMember
) -> None:
    """Test updating a task."""
    task_update(
        who=team_member.user,
        task=task,
        title_description="Hello world",
        assignee=other_team_member,
    )
    task.refresh_from_db()
    assert task.assignee == other_team_member

    assert task.due_date is None

    assert task.assignee
    assert task.assignee.user.email == other_team_member.user.email


def test_task_mark_done(task: Task, team_member: TeamMember) -> None:
    """Test marking a task as done and then not done."""
    assert task.done is None

    task_mark_done(who=team_member.user, task=task, done=True)
    task.refresh_from_db()
    assert task.done is not None

    task_mark_done(who=team_member.user, task=task, done=False)
    task.refresh_from_db()
    assert task.done is None
