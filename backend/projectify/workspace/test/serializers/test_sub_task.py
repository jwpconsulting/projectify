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
"""Test sub task serializers."""
from typing import (
    Any,
    Union,
)
from unittest.mock import MagicMock

import pytest
from rest_framework.request import Request

from projectify.user.models.user import User
from projectify.workspace.models.team_member import TeamMember
from projectify.workspace.services.sub_task import sub_task_create

from ...models import (
    SubTask,
    Task,
)
from ...serializers.sub_task import (
    SubTaskCreateUpdateSerializer,
)

PayloadSingle = Any
Context = dict[str, object]


@pytest.fixture
def payload_single() -> PayloadSingle:
    """Return a single payload for a new sub task."""
    # That's all we need! uuid can't exist yet, description is allowed
    # to be empty
    return {
        "title": "This is a spectacular sub task",
        "done": False,
    }


@pytest.fixture
def user_request(user: User) -> Request:
    """Return a request with a user."""
    user_request = MagicMock()
    user_request.user = user
    return user_request


@pytest.fixture
def context(task: Task, user_request: Request) -> Context:
    """Return serializer context."""
    return {"task": task, "request": user_request}


@pytest.fixture
def sub_tasks(task: Task, team_member: TeamMember) -> list[SubTask]:
    """Create several sub tasks."""
    N = 5
    return [
        sub_task_create(
            who=team_member.user,
            task=task,
            title="don't care",
            done=False,
        )
        for _ in range(N)
    ]


@pytest.mark.django_db
class TestSubTaskListSerializer:
    """Test SubTaskListSerializer."""

    # Serializing just existing stuff
    # I don't assume we will use this serializer to serialize lists
    # of sub tasks, since that is already covered by the default ListSerializer
    # behavior
    def test_empty_list(self) -> None:
        """Test that nothing exciting happens when passing in an empty list."""
        serializer = SubTaskCreateUpdateSerializer([], many=True)
        assert serializer.data == []

    def test_list_existing(self, sub_task: SubTask) -> None:
        """Test that a list containing one instance is returned correctly."""
        serializer = SubTaskCreateUpdateSerializer([sub_task], many=True)
        expected: list[dict[str, Union[str, bool, None]]] = [
            {
                "uuid": str(sub_task.uuid),
                "title": sub_task.title,
                "description": sub_task.description,
                "done": sub_task.done,
            }
        ]
        assert serializer.data == expected

    # Serializing data
    def test_empty_data(self) -> None:
        """Test that nothing exciting happens when data is empty list."""
        serializer = SubTaskCreateUpdateSerializer(data=[], many=True)
        assert serializer.is_valid()
        assert serializer.validated_data == {
            "create_sub_tasks": [],
            "update_sub_tasks": [],
        }

    def test_new_sub_task(
        self,
        payload_single: PayloadSingle,
        context: Context,
    ) -> None:
        """Assert correct behavior when serializing existing task."""
        assert SubTask.objects.count() == 0
        serializer = SubTaskCreateUpdateSerializer(
            data=[payload_single],
            many=True,
            context=context,
        )
        assert serializer.is_valid()
        assert serializer.validated_data == {
            "create_sub_tasks": [
                # Since description is optional, we will receive None back
                # after serialization.
                {**payload_single, "_order": 0, "description": None}
            ],
            "update_sub_tasks": [],
        }
        assert serializer.validated_data == {
            "create_sub_tasks": [
                {
                    "_order": 0,
                    "description": None,
                    "done": False,
                    "title": "This is a spectacular sub task",
                },
            ],
            "update_sub_tasks": [],
        }

    def test_create_no_context(
        self,
        payload_single: PayloadSingle,
        task: Task,
    ) -> None:
        """Test that without a context, we can not create a sub task."""
        assert SubTask.objects.count() == 0
        serializer = SubTaskCreateUpdateSerializer(
            data=[payload_single],
            many=True,
        )
        assert serializer.is_valid()
        assert serializer.validated_data == {
            "create_sub_tasks": [
                {
                    "_order": 0,
                    "description": None,
                    "done": False,
                    "title": "This is a spectacular sub task",
                },
            ],
            "update_sub_tasks": [],
        }

    def test_several_new_sub_tasks(
        self,
        payload_single: PayloadSingle,
        context: Context,
    ) -> None:
        """Assert we can create several new sub tasks."""
        n = 5
        serializer = SubTaskCreateUpdateSerializer(
            data=[payload_single] * n,
            many=True,
            context=context,
        )
        assert serializer.is_valid()
        assert serializer.validated_data == {
            "create_sub_tasks": [
                {
                    "_order": 0,
                    "description": None,
                    "done": False,
                    "title": "This is a spectacular sub task",
                },
                {
                    "_order": 1,
                    "description": None,
                    "done": False,
                    "title": "This is a spectacular sub task",
                },
                {
                    "_order": 2,
                    "description": None,
                    "done": False,
                    "title": "This is a spectacular sub task",
                },
                {
                    "_order": 3,
                    "description": None,
                    "done": False,
                    "title": "This is a spectacular sub task",
                },
                {
                    "_order": 4,
                    "description": None,
                    "done": False,
                    "title": "This is a spectacular sub task",
                },
            ],
            "update_sub_tasks": [],
        }

    def test_update_instance_missing(self, sub_task: SubTask) -> None:
        """Test we get a validation error when instance is missing."""
        serializer = SubTaskCreateUpdateSerializer(
            None,
            data=[
                {
                    "uuid": str(sub_task.uuid),
                    "title": "asd",
                    "done": True,
                }
            ],
            many=True,
        )
        assert serializer.is_valid() is False
        assert (
            "no sub task instances" in serializer.errors["non_field_errors"][0]
        )

    def test_delete_one(self, sub_task: SubTask, context: Context) -> None:
        """Test a sub task is deleted when empty data are passed."""
        assert SubTask.objects.count() == 1
        serializer = SubTaskCreateUpdateSerializer(
            None,
            data=[],
            many=True,
            context=context,
        )
        assert serializer.is_valid(), serializer.errors
        assert serializer.validated_data == {
            "create_sub_tasks": [],
            "update_sub_tasks": [],
        }

    def test_empty_instance_list(self, sub_task: SubTask) -> None:
        """Test that passing an empty instance list will fail."""
        assert SubTask.objects.count() == 1
        serializer = SubTaskCreateUpdateSerializer(
            [],
            data=[{"uuid": str(sub_task.uuid), "title": "n/a", "done": False}],
            many=True,
        )
        assert serializer.is_valid() is False, serializer.errors

    def test_update_existing_sub_task(
        self,
        sub_task: SubTask,
        context: Context,
    ) -> None:
        """Test updating sub task."""
        new_title = "This is a new title, made for this sub task"
        serializer = SubTaskCreateUpdateSerializer(
            None,
            data=[
                {
                    "uuid": str(sub_task.uuid),
                    "title": new_title,
                    "done": True,
                }
            ],
            many=True,
            context=context,
        )
        assert serializer.is_valid(), serializer.errors
        assert serializer.validated_data == {
            "create_sub_tasks": [],
            "update_sub_tasks": [
                {
                    "_order": 0,
                    "description": None,
                    "done": True,
                    "title": "This is a new title, made for this sub task",
                    "uuid": sub_task.uuid,
                }
            ],
        }

    def test_update_several_existing_sub_tasks(
        self,
        task: Task,
        context: Context,
        team_member: TeamMember,
        sub_tasks: list[SubTask],
    ) -> None:
        """Test updating several existing sub tasks."""
        new_title = "fancy factory fabricates fakes"
        serializer = SubTaskCreateUpdateSerializer(
            None,
            data=[
                {
                    "uuid": str(sub_task.uuid),
                    "title": new_title,
                    "done": False,
                }
                for sub_task in sub_tasks
            ],
            many=True,
            context=context,
        )
        assert serializer.is_valid(), serializer.errors
        assert serializer.validated_data == {
            "create_sub_tasks": [],
            "update_sub_tasks": [
                {
                    "_order": 0,
                    "description": None,
                    "done": False,
                    "title": new_title,
                    "uuid": sub_tasks[0].uuid,
                },
                {
                    "_order": 1,
                    "description": None,
                    "done": False,
                    "title": new_title,
                    "uuid": sub_tasks[1].uuid,
                },
                {
                    "_order": 2,
                    "description": None,
                    "done": False,
                    "title": new_title,
                    "uuid": sub_tasks[2].uuid,
                },
                {
                    "_order": 3,
                    "description": None,
                    "done": False,
                    "title": new_title,
                    "uuid": sub_tasks[3].uuid,
                },
                {
                    "_order": 4,
                    "description": None,
                    "done": False,
                    "title": new_title,
                    "uuid": sub_tasks[4].uuid,
                },
            ],
        }

    def test_update_one_create_one(
        self, task: Task, context: Context, sub_task: SubTask
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
        serializer = SubTaskCreateUpdateSerializer(
            None,
            data=[
                # We change the order for some xtra spice
                {"title": new_title, "done": False},
                {
                    "uuid": str(sub_task.uuid),
                    "title": update_title,
                    "done": False,
                },
            ],
            many=True,
            context=context,
        )
        assert serializer.is_valid(), serializer.errors
        assert serializer.validated_data == {
            "create_sub_tasks": [
                {
                    "_order": 0,
                    "description": None,
                    "done": False,
                    "title": new_title,
                }
            ],
            "update_sub_tasks": [
                {
                    "_order": 1,
                    "description": None,
                    "done": False,
                    "title": update_title,
                    "uuid": sub_task.uuid,
                }
            ],
        }

    def test_change_order(
        self, sub_tasks: list[SubTask], task: Task, context: Context
    ) -> None:
        """Test changing the order of several sub tasks."""
        a, b, c, d, e = sub_tasks
        title = "asd"
        serializer = SubTaskCreateUpdateSerializer(
            None,
            data=[
                {
                    "uuid": str(c.uuid),
                    "title": title,
                    "done": False,
                },
                {
                    "uuid": str(b.uuid),
                    "title": title,
                    "done": False,
                },
                {
                    "uuid": str(d.uuid),
                    "title": title,
                    "done": False,
                },
                {
                    "uuid": str(a.uuid),
                    "title": title,
                    "done": False,
                },
                {
                    "uuid": str(e.uuid),
                    "title": title,
                    "done": False,
                },
            ],
            many=True,
            context=context,
        )
        assert serializer.is_valid(), serializer.errors
        assert serializer.validated_data == {
            "create_sub_tasks": [],
            "update_sub_tasks": [
                {
                    "_order": 0,
                    "description": None,
                    "done": False,
                    "title": title,
                    "uuid": c.uuid,
                },
                {
                    "_order": 1,
                    "description": None,
                    "done": False,
                    "title": title,
                    "uuid": b.uuid,
                },
                {
                    "_order": 2,
                    "description": None,
                    "done": False,
                    "title": title,
                    "uuid": d.uuid,
                },
                {
                    "_order": 3,
                    "description": None,
                    "done": False,
                    "title": title,
                    "uuid": a.uuid,
                },
                {
                    "_order": 4,
                    "description": None,
                    "done": False,
                    "title": title,
                    "uuid": e.uuid,
                },
            ],
        }

    def test_create_one_delete_one(
        self, task: Task, context: Context, sub_task: SubTask
    ) -> None:
        """
        Test creating and deleting.

        1) The new sub task shall be created
        2) The missing sub task shall be deleted
        """
        title = "new sub task who dis"
        assert task.subtask_set.count() == 1
        serializer = SubTaskCreateUpdateSerializer(
            None,
            data=[
                {"title": title, "done": False},
            ],
            many=True,
            context=context,
        )
        assert serializer.is_valid(), serializer.errors
        assert serializer.validated_data == {
            "create_sub_tasks": [
                {
                    "_order": 0,
                    "description": None,
                    "done": False,
                    "title": title,
                }
            ],
            "update_sub_tasks": [],
        }

    def test_create_and_change_order(
        self,
        task: Task,
        context: Context,
        sub_tasks: list[SubTask],
    ) -> None:
        """
        Test creating sub tasks and changing the order of existing ones.

        1) The new tasks shall be inserted at the right place.
        2) Updated tasks shall be moved.
        """
        a, b, _c, _d, _e = sub_tasks
        title = "asd"
        new_title = "i am a new sub task"
        serializer = SubTaskCreateUpdateSerializer(
            None,
            data=[
                {
                    "title": new_title,
                    "done": False,
                },
                {
                    "uuid": str(b.uuid),
                    "title": title,
                    "done": False,
                },
                {
                    "title": new_title,
                    "done": False,
                },
                {
                    "uuid": str(a.uuid),
                    "title": title,
                    "done": False,
                },
            ],
            many=True,
            context=context,
        )
        assert serializer.is_valid(), serializer.errors
        assert serializer.validated_data == {
            "create_sub_tasks": [
                {
                    "_order": 0,
                    "description": None,
                    "done": False,
                    "title": new_title,
                },
                {
                    "_order": 2,
                    "description": None,
                    "done": False,
                    "title": new_title,
                },
            ],
            "update_sub_tasks": [
                {
                    "_order": 1,
                    "description": None,
                    "done": False,
                    "title": title,
                    "uuid": b.uuid,
                },
                {
                    "_order": 3,
                    "description": None,
                    "done": False,
                    "title": title,
                    "uuid": a.uuid,
                },
            ],
        }
