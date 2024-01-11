# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Copyright (C) 2023-2024 JWP Consulting GK
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
"""Test sub task model services."""
from typing import (
    Sequence,
)
from uuid import UUID

import pytest

from ...models import (
    SubTask,
    Task,
)
from ...models.workspace_user import WorkspaceUser
from ...services.sub_task import (
    ValidatedData,
    ValidatedDatum,
    sub_task_create,
    sub_task_create_many,
    sub_task_update_many,
)

pytestmark = pytest.mark.django_db


def test_add_sub_task(task: Task, workspace_user: WorkspaceUser) -> None:
    """Test adding a sub task."""
    assert task.subtask_set.count() == 0
    sub_task_create(
        who=workspace_user.user,
        task=task,
        title="don't care",
        done=False,
    )
    assert task.subtask_set.count() == 1


@pytest.fixture
def sub_tasks(task: Task, workspace_user: WorkspaceUser) -> Sequence[SubTask]:
    """Create several sub tasks."""
    N = 5
    return [
        sub_task_create(
            who=workspace_user.user,
            task=task,
            title="don't care",
            done=False,
        )
        for _ in range(N)
    ]


def test_new_sub_task(
    workspace_user: WorkspaceUser,
    task: Task,
) -> None:
    """Assert we can create a new sub task."""
    payload_single: ValidatedDatum = {
        "title": "This is a spectacular sub task",
        "done": False,
        "_order": 0,
    }
    assert SubTask.objects.count() == 0
    sub_task_create_many(
        who=workspace_user.user,
        task=task,
        create_sub_tasks=[payload_single],
    )
    assert SubTask.objects.count() == 1
    new_sub_task = SubTask.objects.get()
    assert new_sub_task.title == payload_single["title"]
    assert new_sub_task.done == payload_single["done"]


def test_several_new_sub_tasks(
    task: Task,
    workspace_user: WorkspaceUser,
) -> None:
    """Assert we can create several new sub tasks."""
    create_sub_tasks: list[ValidatedDatum] = [
        {"title": "one", "_order": 0, "done": False},
        {"title": "two", "_order": 1, "done": False},
        {"title": "three", "_order": 2, "done": False},
        {"title": "four", "_order": 3, "done": False},
        {"title": "five", "_order": 4, "done": False},
    ]
    sub_task_create_many(
        create_sub_tasks=create_sub_tasks,
        task=task,
        who=workspace_user.user,
    )
    assert SubTask.objects.count() == len(create_sub_tasks)


def test_delete_one(
    workspace_user: WorkspaceUser,
    sub_task: SubTask,
) -> None:
    """Test a sub task is deleted when empty data are passed."""
    assert SubTask.objects.count() == 1
    validated_data: ValidatedData = {
        "create_sub_tasks": [],
        "update_sub_tasks": [],
    }
    sub_task_update_many(
        who=workspace_user.user,
        task=sub_task.task,
        sub_tasks=[sub_task],
        validated_data=validated_data,
    )
    assert SubTask.objects.count() == 0, SubTask.objects.all()


def test_update_existing_sub_task(
    sub_task: SubTask,
    workspace_user: WorkspaceUser,
) -> None:
    """Test updating sub task."""
    new_title = "This is a new title, made for this sub task"
    validated_data: ValidatedData = {
        "update_sub_tasks": [
            {
                "uuid": sub_task.uuid,
                "title": new_title,
                "done": True,
                "_order": 0,
            }
        ],
        "create_sub_tasks": None,
    }
    sub_task_update_many(
        who=workspace_user.user,
        task=sub_task.task,
        sub_tasks=[sub_task],
        validated_data=validated_data,
    )
    assert SubTask.objects.count() == 1
    sub_task.refresh_from_db()
    assert sub_task.title == new_title


def test_update_several_existing_sub_tasks(
    task: Task,
    workspace_user: WorkspaceUser,
    sub_tasks: list[SubTask],
) -> None:
    """Test updating several existing sub tasks."""
    new_title = "fancy factory fabricates fakes"
    validated_data: ValidatedData = {
        "update_sub_tasks": [
            {
                "uuid": sub_task.uuid,
                "title": new_title,
                "done": False,
                "_order": n,
            }
            for n, sub_task in enumerate(sub_tasks)
        ],
        "create_sub_tasks": [],
    }
    sub_task_update_many(
        validated_data=validated_data,
        sub_tasks=sub_tasks,
        who=workspace_user.user,
        task=task,
    )
    assert SubTask.objects.count() == len(sub_tasks)
    for sub_task in task.subtask_set.all():
        assert sub_task.title == new_title


def test_update_one_create_one(
    task: Task,
    workspace_user: WorkspaceUser,
    sub_task: SubTask,
) -> None:
    """
    Test with multiple sub tasks.

    1) Order shall be adjusted
    2) New sub task shall be created
    3) Existing sub task title shall be updated
    """
    assert task.subtask_set.count() == 1
    update_title = "Foo the bar, baz the flub"
    new_title = "I am complete, new and creative, hello"
    validated_data: ValidatedData = {
        "create_sub_tasks": [
            {"title": new_title, "done": False, "_order": 0},
        ],
        "update_sub_tasks": [
            {
                "uuid": sub_task.uuid,
                "title": update_title,
                "done": False,
                "_order": 1,
            },
        ],
    }

    sub_task_update_many(
        validated_data=validated_data,
        sub_tasks=[sub_task],
        who=workspace_user.user,
        task=task,
    )
    assert task.subtask_set.count() == 2
    a, b = task.subtask_set.all()
    assert a.title == new_title
    assert b.title == update_title


def test_change_order(
    sub_tasks: list[SubTask],
    task: Task,
    workspace_user: WorkspaceUser,
) -> None:
    """Test changing the order of several sub tasks."""
    a, b, c, d, e = sub_tasks
    title = "asd"
    validated_data: ValidatedData = {
        "create_sub_tasks": [],
        "update_sub_tasks": [
            {
                "uuid": c.uuid,
                "title": title,
                "done": False,
                "_order": 0,
            },
            {
                "uuid": b.uuid,
                "title": title,
                "done": False,
                "_order": 1,
            },
            {
                "uuid": d.uuid,
                "title": title,
                "done": False,
                "_order": 2,
            },
            {
                "uuid": a.uuid,
                "title": title,
                "done": False,
                "_order": 3,
            },
            {
                "uuid": e.uuid,
                "title": title,
                "done": False,
                "_order": 4,
            },
        ],
    }
    sub_task_update_many(
        validated_data=validated_data,
        sub_tasks=sub_tasks,
        who=workspace_user.user,
        task=task,
    )
    assert SubTask.objects.count() == len(sub_tasks)
    new_order: list[UUID] = list(
        task.subtask_set.values_list("uuid", flat=True)
    )
    assert new_order == [c.uuid, b.uuid, d.uuid, a.uuid, e.uuid]


def test_create_one_delete_one(
    task: Task, sub_task: SubTask, workspace_user: WorkspaceUser
) -> None:
    """
    Test creating and deleting.

    1) The new sub task shall be created
    2) The missing sub task shall be deleted
    """
    assert task.subtask_set.count() == 1
    validated_data: ValidatedData = {
        "create_sub_tasks": [
            {"title": "new sub task who dis", "done": False, "_order": 0},
        ],
        "update_sub_tasks": [],
    }
    sub_task_update_many(
        validated_data=validated_data,
        sub_tasks=[sub_task],
        who=workspace_user.user,
        task=task,
    )

    assert task.subtask_set.count() == 1
    new_sub_task = task.subtask_set.get()
    assert new_sub_task.title == "new sub task who dis"
    assert new_sub_task.uuid != sub_task.uuid


def test_create_and_change_order(
    task: Task, workspace_user: WorkspaceUser, sub_tasks: list[SubTask]
) -> None:
    """
    Test creating sub tasks and changing the order of existing ones.

    1) The new tasks shall be inserted at the right place.
    2) Updated tasks shall be moved.
    """
    a, b, _c, _d, _e = sub_tasks
    title = "asd"
    new_title = "i am a new sub task"
    validated_data: ValidatedData = {
        "create_sub_tasks": [
            {
                "title": new_title,
                "done": False,
                "_order": 0,
            },
            {
                "title": new_title,
                "done": False,
                "_order": 2,
            },
        ],
        "update_sub_tasks": [
            {
                "uuid": b.uuid,
                "title": title,
                "done": False,
                "_order": 1,
            },
            {
                "uuid": a.uuid,
                "title": title,
                "done": False,
                "_order": 3,
            },
        ],
    }
    sub_task_update_many(
        validated_data=validated_data,
        sub_tasks=sub_tasks,
        who=workspace_user.user,
        task=task,
    )
    assert SubTask.objects.count() == 4
    new_order: list[UUID] = list(
        task.subtask_set.values_list("uuid", flat=True)
    )
    assert new_order[1] == b.uuid, new_order
    assert new_order[3] == a.uuid, new_order
