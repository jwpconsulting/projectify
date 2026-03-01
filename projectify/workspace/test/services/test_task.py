# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023 JWP Consulting GK
"""Test task services."""

from datetime import datetime

import pytest
from rest_framework import exceptions

from projectify.workspace.services.label import label_create

from ...models import Label, Project, Section, Task, TeamMember, Workspace
from ...services.task import (
    task_assign_labels,
    task_create_nested,
    task_mark_done,
    task_move_after,
    task_update_nested,
)

pytestmark = pytest.mark.django_db


def test_set_labels(
    task: Task,
    labels: list[Label],
    unrelated_workspace: Workspace,
    unrelated_team_member: TeamMember,
) -> None:
    """Test setting labels."""
    assert task.labels.count() == 0
    a, b, c, d, e = labels
    task_assign_labels(task=task, labels=[a, b])
    assert task.labels.count() == 2
    # The order is inverted since we are not actually sorting by the
    # TaskLabel creation but the default ordering of the label itself
    # Furthermore, we work independently of the service layer, so it is
    # questionable how useful this code is to the application
    # TODO refactor
    assert list(task.labels.values_list("id", flat=True)) == [b.id, a.id]
    task_assign_labels(task=task, labels=[c, d, e])
    assert task.labels.count() == 3
    assert list(task.labels.values_list("id", flat=True)) == [
        e.id,
        d.id,
        c.id,
    ]
    task_assign_labels(task=task, labels=[])
    assert task.labels.count() == 0
    assert list(task.labels.values_list("id", flat=True)) == []

    unrelated = label_create(
        workspace=unrelated_workspace,
        who=unrelated_team_member.user,
        color=0,
        name="don't care",
    )
    task_assign_labels(task=task, labels=[unrelated])
    assert task.labels.count() == 0
    assert list(task.labels.values_list("id", flat=True)) == []


# Create
def test_create_task(
    section: Section,
    team_member: TeamMember,
    other_team_member: TeamMember,
) -> None:
    """Test adding tasks to a project."""
    count = section.task_set.count()
    task = task_create_nested(
        who=team_member.user,
        section=section,
        title="foo",
        description="bar",
    )
    assert section.task_set.count() == count + 1
    task2 = task_create_nested(
        who=team_member.user,
        section=section,
        title="foo",
        description="bar",
        assignee=other_team_member,
    )
    assert section.task_set.count() == count + 2
    assert list(section.task_set.all()) == [task, task2]


def test_create_task_unrelated_teammember(
    section: Section,
    team_member: TeamMember,
    unrelated_team_member: TeamMember,
) -> None:
    """Test adding tasks to a project."""
    with pytest.raises(exceptions.ValidationError) as e:
        task_create_nested(
            who=team_member.user,
            section=section,
            title="foo",
            assignee=unrelated_team_member,
        )
    assert e.match("belongs to a different workspace")


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
    )
    assert list(task.labels.values_list("uuid", flat=True)) == [label.uuid]
    assert task.assignee == team_member


def test_add_task_due_date(
    section: Section,
    team_member: TeamMember,
    now: datetime,
) -> None:
    """Test adding a task with a due date."""
    task = task_create_nested(
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
) -> None:
    """Test updating a task."""
    task_update_nested(
        who=team_member.user,
        task=task,
        title="Hello world",
        description=None,
        assignee=other_team_member,
        labels=[label],
    )
    task.refresh_from_db()
    assert task.assignee == other_team_member

    assert task.due_date is None

    assert list(task.labels.values_list("uuid", flat=True)) == [label.uuid]

    assert task.assignee
    assert task.assignee.user.email == other_team_member.user.email


def test_moving_task_within_section(
    section: Section,
    task: Task,
    team_member: TeamMember,
) -> None:
    """Test moving a task around within the same section."""
    other_task = task_create_nested(
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
    task_move_after(
        who=team_member.user,
        task=task,
        after=section,
    )
    assert list(section.task_set.all()) == [
        task,
        other_task,
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
    other_task = task_create_nested(
        who=team_member.user,
        title="don't care",
        section=section,
    )
    assert list(section.task_set.all()) == [
        task,
        other_task,
    ]
    other_section_task = task_create_nested(
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


def test_task_mark_done(
    task: Task,
    team_member: TeamMember,
) -> None:
    """Test marking a task as done and then not done."""
    assert task.done is None

    task_mark_done(who=team_member.user, task=task, done=True)
    task.refresh_from_db()
    assert task.done is not None

    task_mark_done(who=team_member.user, task=task, done=False)
    task.refresh_from_db()
    assert task.done is None
