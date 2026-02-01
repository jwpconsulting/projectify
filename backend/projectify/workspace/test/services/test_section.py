# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023 JWP Consulting GK
"""Test section services."""

import pytest

from projectify.workspace.models import Project
from projectify.workspace.models.section import Section
from projectify.workspace.models.task import Task
from projectify.workspace.models.team_member import TeamMember
from projectify.workspace.services.section import (
    section_delete,
    section_minimize,
    section_move,
    section_move_in_direction,
)

pytestmark = pytest.mark.django_db


def test_delete_non_empty_section(
    team_member: TeamMember,
    section: Section,
    # Make sure there is a task
    task: Task,
) -> None:
    """Assert we can delete a non-empty section."""
    count = Section.objects.count()
    task_count = Task.objects.count()
    section_delete(
        section=section,
        who=team_member.user,
    )
    assert Section.objects.count() == count - 1
    assert Task.objects.count() == task_count - 1


def test_moving_section(
    project: Project,
    section: Section,
    other_section: Section,
    other_other_section: Section,
    team_member: TeamMember,
) -> None:
    """Test moving a section around."""
    assert list(project.section_set.all()) == [
        section,
        other_section,
        other_other_section,
    ]
    section_move(
        section=section,
        order=0,
        who=team_member.user,
    )
    assert list(project.section_set.all()) == [
        section,
        other_section,
        other_other_section,
    ]
    section_move(
        section=section,
        order=2,
        who=team_member.user,
    )
    assert list(project.section_set.all()) == [
        other_section,
        other_other_section,
        section,
    ]
    section_move(
        section=section,
        order=1,
        who=team_member.user,
    )
    assert list(project.section_set.all()) == [
        other_section,
        section,
        other_other_section,
    ]


def test_moving_empty_section(
    project: Project,
    section: Section,
    team_member: TeamMember,
) -> None:
    """Test moving when there are no other sections."""
    assert list(project.section_set.all()) == [
        section,
    ]
    section_move(
        section=section,
        order=1,
        who=team_member.user,
    )
    assert list(project.section_set.all()) == [
        section,
    ]
    assert section._order == 0


def test_section_move_in_direction_up(
    project: Project,
    section: Section,
    other_section: Section,
    other_other_section: Section,
    team_member: TeamMember,
) -> None:
    """Test moving a section up."""
    assert list(project.section_set.all()) == [
        section,
        other_section,
        other_other_section,
    ]

    section_move_in_direction(
        section=other_section,
        direction="up",
        who=team_member.user,
    )
    assert list(project.section_set.all()) == [
        other_section,
        section,
        other_other_section,
    ]


def test_section_move_in_direction_down(
    project: Project,
    section: Section,
    other_section: Section,
    other_other_section: Section,
    team_member: TeamMember,
) -> None:
    """Test moving a section down."""
    assert list(project.section_set.all()) == [
        section,
        other_section,
        other_other_section,
    ]

    section_move_in_direction(
        section=section,
        direction="down",
        who=team_member.user,
    )
    assert list(project.section_set.all()) == [
        other_section,
        section,
        other_other_section,
    ]


def test_section_move_in_direction_up_at_top(
    project: Project,
    section: Section,
    other_section: Section,
    team_member: TeamMember,
) -> None:
    """Test moving a section up when it's already at the top."""
    assert list(project.section_set.all()) == [
        section,
        other_section,
    ]

    section_move_in_direction(
        section=section,
        direction="up",
        who=team_member.user,
    )
    assert list(project.section_set.all()) == [
        section,
        other_section,
    ]


def test_section_move_in_direction_down_at_bottom(
    project: Project,
    section: Section,
    other_section: Section,
    team_member: TeamMember,
) -> None:
    """Test moving a section down when it's already at the bottom."""
    assert list(project.section_set.all()) == [
        section,
        other_section,
    ]

    section_move_in_direction(
        section=other_section,
        direction="down",
        who=team_member.user,
    )
    assert list(project.section_set.all()) == [
        section,
        other_section,
    ]


def test_section_move_in_direction_single_section(
    project: Project,
    section: Section,
    team_member: TeamMember,
) -> None:
    """Test moving when there's only one section."""
    assert list(project.section_set.all()) == [section]
    section_move_in_direction(
        section=section,
        direction="up",
        who=team_member.user,
    )
    assert list(project.section_set.all()) == [section]
    section_move_in_direction(
        section=section,
        direction="down",
        who=team_member.user,
    )
    assert list(project.section_set.all()) == [section]


@pytest.mark.django_db
def test_section_minimize(team_member: TeamMember, section: Section) -> None:
    """Test minimizing and expanding a section."""
    assert section.minimized_by.count() == 0

    section_minimize(who=team_member.user, section=section, minimized=True)

    assert section.minimized_by.count() == 1
    assert team_member.user in section.minimized_by.all()

    section_minimize(who=team_member.user, section=section, minimized=False)
    assert section.minimized_by.count() == 0
    assert team_member.user not in section.minimized_by.all()
