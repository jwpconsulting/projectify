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

from workspace.models import WorkspaceBoard
from workspace.models.task import Task
from workspace.models.workspace_board_section import WorkspaceBoardSection
from workspace.models.workspace_user import WorkspaceUser
from workspace.services.task import task_create, task_move_after


# Create
@pytest.mark.django_db
def test_create_task(
    workspace_board_section: WorkspaceBoardSection,
    workspace_user: WorkspaceUser,
) -> None:
    """Test adding tasks to a workspace board."""
    assert workspace_board_section.task_set.count() == 0
    task = task_create(
        who=workspace_user.user,
        workspace_board_section=workspace_board_section,
        title="foo",
        description="bar",
    )
    assert workspace_board_section.task_set.count() == 1
    task2 = task_create(
        who=workspace_user.user,
        workspace_board_section=workspace_board_section,
        title="foo",
        description="bar",
    )
    assert workspace_board_section.task_set.count() == 2
    assert list(workspace_board_section.task_set.all()) == [task, task2]


@pytest.mark.django_db
def test_add_task_deadline(
    workspace_board_section: WorkspaceBoardSection,
    workspace_user: WorkspaceUser,
    now: datetime,
) -> None:
    """Test adding a task with a deadline."""
    task = task_create(
        workspace_board_section=workspace_board_section,
        who=workspace_user.user,
        title="foo",
        description="bar",
        deadline=now,
    )
    assert task.deadline is not None


@pytest.mark.django_db
def test_moving_task_within_section(
    workspace_board_section: WorkspaceBoardSection,
    task: Task,
    workspace_user: WorkspaceUser,
) -> None:
    """Test moving a task around within the same section."""
    other_task = task_create(
        who=workspace_user.user,
        title="don't care",
        workspace_board_section=workspace_board_section,
    )
    assert list(workspace_board_section.task_set.all()) == [
        task,
        other_task,
    ]
    task_move_after(
        who=workspace_user.user,
        task=task,
        after=other_task,
    )
    assert list(workspace_board_section.task_set.all()) == [
        other_task,
        task,
    ]


@pytest.mark.django_db
def test_moving_task_to_other_section(
    # TODO this fixture might not be needed
    workspace_board: WorkspaceBoard,
    workspace_board_section: WorkspaceBoardSection,
    other_workspace_board_section: WorkspaceBoardSection,
    task: Task,
    workspace_user: WorkspaceUser,
) -> None:
    """Test moving a task around to another section."""
    other_task = task_create(
        who=workspace_user.user,
        title="don't care",
        workspace_board_section=workspace_board_section,
    )
    assert list(workspace_board_section.task_set.all()) == [
        task,
        other_task,
    ]
    other_section_task = task_create(
        who=workspace_user.user,
        title="don't care",
        workspace_board_section=other_workspace_board_section,
    )
    assert list(other_workspace_board_section.task_set.all()) == [
        other_section_task,
    ]
    task_move_after(
        who=workspace_user.user,
        task=task,
        after=other_workspace_board_section,
    )
    assert list(other_workspace_board_section.task_set.all()) == [
        task,
        other_section_task,
    ]


@pytest.mark.django_db
def test_moving_task_to_empty_section(
    # TODO the following two fixtures might not be needed
    workspace_board: WorkspaceBoard,
    workspace_board_section: WorkspaceBoardSection,
    other_workspace_board_section: WorkspaceBoardSection,
    task: Task,
    workspace_user: WorkspaceUser,
) -> None:
    """
    Test what happens if we move it into an empty section.

    We also see what happens when the id is set too high.
    """
    task_move_after(
        who=workspace_user.user,
        task=task,
        after=other_workspace_board_section,
    )
    assert list(other_workspace_board_section.task_set.all()) == [
        task,
    ]
    task.refresh_from_db()
    assert task._order == 0
