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
"""Test workspace serializer."""
from typing import Any
from unittest.mock import MagicMock
from uuid import uuid4

import pytest
from faker import Faker
from rest_framework.request import Request

from projectify.user.models.user import User

from ...models.label import Label
from ...models.section import Section
from ...models.sub_task import SubTask
from ...models.task import Task
from ...models.team_member import TeamMember
from ...models.workspace import Workspace
from ...serializers.task_detail import (
    TaskCreateSerializer,
    TaskDetailSerializer,
    TaskUpdateSerializer,
)
from ...services.sub_task import sub_task_create

pytestmark = pytest.mark.django_db


PayloadSingle = Any
Context = dict[str, object]


@pytest.fixture
def user_request(user: User) -> Request:
    """Return a request with a user."""
    user_request = MagicMock()
    user_request.user = user
    return user_request


@pytest.fixture
def context(user_request: Request) -> Context:
    """Return serializer context."""
    return {"request": user_request}


@pytest.fixture
def payload_single() -> PayloadSingle:
    """Return a single payload for a new sub task."""
    # That's all we need! uuid can't exist yet, description is allowed
    # to be empty
    return {
        "title": "This is a spectacular sub task",
        "done": False,
        "description": None,
    }


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


@pytest.fixture
def create_task_payload(section: Section, faker: Faker) -> Any:
    """Create payload for task to be created."""
    return {
        "title": faker.name(),
        "section": {"uuid": str(section.uuid)},
        "description": None,
        "assignee": None,
        "labels": [],
        "due_date": None,
    }


@pytest.fixture
def validated_data_create(section: Section, create_task_payload: Any) -> Any:
    """
    Return what we think most of the validated data should look like.

    Overwrite and adjust where needed.
    """
    return {
        **create_task_payload,
        "section": section,
        "workspace": section.project.workspace,
    }


@pytest.fixture
def update_task_payload(task: Task) -> Any:
    """Create payload for task to be updated."""
    return {
        "title": task.title,
        "description": None,
        "assignee": None,
        "labels": [],
        "due_date": None,
    }


@pytest.fixture
def validated_data_update(task: Task) -> Any:
    """
    Return what we think most of the validated data should look like.

    Overwrite and adjust where needed.
    """
    return {
        "title": task.title,
        "workspace": task.workspace,
        "description": None,
        "assignee": None,
        "labels": [],
        "due_date": None,
    }


class TestTaskDetailSerializer:
    """Test the task detail serializer."""

    def test_readonly_fields(self, task: Task) -> None:
        """Check that fields are actually readonly by trying a few."""
        serializer = TaskDetailSerializer(
            task,
            data={
                "title": task.title,
                "description": None,
                "number": 133337,
                "uuid": 2,
                "due_date": None,
            },
        )
        # it is_valid, because DRF just ignores the read only fields inside
        # data
        serializer.is_valid(raise_exception=True)
        # Here we prove that DRF ignores "number" and other r/o fields
        assert "number" not in serializer.validated_data
        assert "uuid" not in serializer.validated_data
        assert "title" in serializer.validated_data


class TestTaskCreateSerializer:
    """Test the task update serializer."""

    def test_readonly_fields(
        self,
        task: Task,
        workspace: Workspace,
        team_member: TeamMember,
        section: Section,
        context: Context,
    ) -> None:
        """Check that fields are actually readonly by trying a few."""
        task.assignee = team_member
        task.save()
        serializer = TaskCreateSerializer(
            task,
            data={
                "title": task.title,
                "description": None,
                "number": 133337,
                "uuid": 2,
                "labels": [],
                "assignee": None,
                "section": {
                    "uuid": str(section.uuid),
                },
                "due_date": None,
            },
            context=context,
        )
        # it is_valid, because DRF just ignores the read only fields inside
        # data
        serializer.is_valid(raise_exception=True)
        # Here we prove that DRF ignores "number" and other r/o fields
        assert serializer.validated_data == {
            "assignee": None,
            "labels": [],
            "title": task.title,
            "description": None,
            "workspace": workspace,
            "section": section,
            "due_date": None,
        }

    def test_create(
        self,
        label: Label,
        workspace: Workspace,
        team_member: TeamMember,
        section: Section,
        context: Context,
    ) -> None:
        """Test creating a task."""
        serializer = TaskCreateSerializer(
            data={
                "title": "This is a great task title.",
                "description": None,
                "labels": [{"uuid": str(label.uuid)}],
                "assignee": {"uuid": str(team_member.uuid)},
                "section": {
                    "uuid": str(section.uuid),
                },
                "due_date": None,
            },
            context=context,
        )
        serializer.is_valid(raise_exception=True)
        assert serializer.validated_data == {
            "assignee": team_member,
            "labels": [label],
            "title": "This is a great task title.",
            "description": None,
            "workspace": workspace,
            "section": section,
            "due_date": None,
        }

    def test_create_unrelated_section(
        self,
        context: Context,
        unrelated_section: Section,
    ) -> None:
        """Test creating a task but the ws board section is wrong."""
        serializer = TaskCreateSerializer(
            data={
                "title": "This is a great task title.",
                "labels": [],
                "assignee": None,
                "section": {
                    "uuid": str(unrelated_section.uuid),
                },
            },
            context=context,
        )
        assert not serializer.is_valid()
        assert serializer.errors["section"]

    def test_create_no_sub_tasks(
        self,
        create_task_payload: Any,
        validated_data_create: Any,
        context: Context,
    ) -> None:
        """Test that nothing exciting happens when passing no sub tasks."""
        serializer = TaskCreateSerializer(
            data={**create_task_payload, "sub_tasks": []},
            context=context,
        )
        assert serializer.is_valid()
        assert serializer.validated_data == {
            **validated_data_create,
            "sub_tasks": {"create_sub_tasks": [], "update_sub_tasks": []},
        }


class TestTaskUpdateSerializer:
    """Test TaskUpdateSerializer."""

    def test_update(
        self,
        task: Task,
        label: Label,
        team_member: TeamMember,
        workspace: Workspace,
        sub_task: SubTask,
        user_request: Request,
    ) -> None:
        """Test updating a task."""
        assert len(task.subtask_set.all()) == 1
        assert task.due_date is not None
        due_date = task.due_date
        serializer = TaskUpdateSerializer(
            task,
            data={
                "title": task.title,
                "description": None,
                "labels": [{"uuid": str(label.uuid)}],
                "assignee": {"uuid": str(team_member.uuid)},
                "due_date": due_date.isoformat(),
                "sub_tasks": [
                    {
                        "title": "Frobnice fluffballs",
                        "done": True,
                    },
                    {
                        "uuid": str(sub_task.uuid),
                        "title": "Settle Catan",
                        "done": not sub_task.done,
                    },
                    {
                        "title": "Frebnecize flerfbowls",
                        "done": True,
                    },
                ],
            },
            context={"request": user_request},
        )
        assert serializer.is_valid(), serializer.errors
        assert serializer.validated_data == {
            "assignee": team_member,
            "due_date": due_date,
            "labels": [label],
            "sub_tasks": {
                "create_sub_tasks": [
                    {
                        "_order": 0,
                        "description": None,
                        "done": True,
                        "title": "Frobnice fluffballs",
                    },
                    {
                        "_order": 2,
                        "description": None,
                        "done": True,
                        "title": "Frebnecize flerfbowls",
                    },
                ],
                "update_sub_tasks": [
                    {
                        "_order": 1,
                        "description": None,
                        "done": not sub_task.done,
                        "title": "Settle Catan",
                        "uuid": sub_task.uuid,
                    }
                ],
            },
            "title": task.title,
            "description": None,
            "workspace": workspace,
        }

    def test_update_missing_label(
        self, task: Task, label: Label, unrelated_label: Label
    ) -> None:
        """Test updating with an unrelated label."""
        serializer = TaskUpdateSerializer(
            task,
            data={
                "title": task.title,
                "description": None,
                "labels": [
                    {"uuid": str(label.uuid)},
                    {"uuid": str(unrelated_label.uuid)},
                ],
                "assignee": None,
                "due_date": None,
            },
            context=context,
        )
        assert not serializer.is_valid(), serializer.validated_data
        assert serializer.errors == {
            "labels": [{}, {"uuid": "This label could not be found"}]
        }

    def test_update_wrong_assignee(
        self, task: Task, unrelated_team_member: TeamMember
    ) -> None:
        """Test updating a task."""
        serializer = TaskUpdateSerializer(
            task,
            data={
                "title": task.title,
                "description": None,
                "labels": [],
                "assignee": {"uuid": str(unrelated_team_member.uuid)},
                "due_date": None,
            },
            context=context,
        )
        assert not serializer.is_valid()
        (error,) = serializer.errors["assignee"]
        assert "could not be found" in error

    def test_update_one_existing_sub_task(
        self,
        task: Task,
        update_task_payload: Any,
        sub_task: SubTask,
        validated_data_update: Any,
    ) -> None:
        """Test that a list containing one instance is returned correctly."""
        payload = {
            "title": sub_task.title,
            "description": sub_task.description,
            "done": sub_task.done,
        }
        serializer = TaskUpdateSerializer(
            task,
            data={
                **update_task_payload,
                "sub_tasks": [{**payload, "uuid": str(sub_task.uuid)}],
            },
        )
        assert serializer.is_valid()
        expected = {
            **validated_data_update,
            "sub_tasks": {
                "create_sub_tasks": [],
                "update_sub_tasks": [
                    {**payload, "_order": 0, "uuid": sub_task.uuid}
                ],
            },
        }
        assert serializer.validated_data == expected

    # Serializing data
    def test_update_no_sub_tasks(
        self, task: Task, validated_data_update: Any, update_task_payload: Any
    ) -> None:
        """Test behavior when updating task with no sub tasks."""
        serializer = TaskUpdateSerializer(task, data=update_task_payload)
        assert serializer.is_valid()
        assert serializer.validated_data == validated_data_update

    def test_update_new_sub_task(
        self,
        task: Task,
        payload_single: PayloadSingle,
        update_task_payload: Any,
        validated_data_update: Any,
        context: Context,
    ) -> None:
        """Assert correct behavior when serializing existing task."""
        serializer = TaskUpdateSerializer(
            task,
            data={**update_task_payload, "sub_tasks": [payload_single]},
            context=context,
        )
        assert serializer.is_valid()
        assert serializer.validated_data == {
            **validated_data_update,
            "sub_tasks": {
                "create_sub_tasks": [
                    # Since description is optional, we will receive None back
                    # after serialization.
                    {**payload_single, "_order": 0, "description": None}
                ],
                "update_sub_tasks": [],
            },
        }

    def test_update_several_new_sub_tasks(
        self,
        task: Task,
        payload_single: PayloadSingle,
        update_task_payload: Any,
        validated_data_update: Any,
        context: Context,
    ) -> None:
        """Assert we can create several new sub tasks."""
        n = 5
        serializer = TaskUpdateSerializer(
            task,
            data={**update_task_payload, "sub_tasks": [payload_single] * n},
            context=context,
        )
        assert serializer.is_valid(), serializer.errors
        assert serializer.validated_data == {
            **validated_data_update,
            "sub_tasks": {
                "create_sub_tasks": [
                    {**payload_single, "_order": 0},
                    {**payload_single, "_order": 1},
                    {**payload_single, "_order": 2},
                    {**payload_single, "_order": 3},
                    {**payload_single, "_order": 4},
                ],
                "update_sub_tasks": [],
            },
        }

    def test_update_instance_missing(
        self,
        sub_task: SubTask,
        context: Context,
        task: Task,
        update_task_payload: Any,
    ) -> None:
        """Test we get a validation error when instance is missing."""
        uuid = uuid4()
        serializer = TaskUpdateSerializer(
            task,
            data={
                **update_task_payload,
                "sub_tasks": [
                    {"uuid": str(uuid), "title": "asd", "done": True}
                ],
            },
            context=context,
        )
        assert serializer.is_valid() is False
        assert serializer.errors == {
            "sub_tasks": [
                {
                    "uuid": f"Sub task {uuid} could not be found amount the instance data. Check whether you have correctly passed all task's sub task instances."
                }
            ]
        }

    def test_update_delete_sub_task(
        self,
        sub_task: SubTask,
        context: Context,
        task: Task,
        update_task_payload: Any,
        validated_data_update: Any,
    ) -> None:
        """Test a sub task is deleted when empty data are passed."""
        assert SubTask.objects.get() == sub_task
        serializer = TaskUpdateSerializer(
            task,
            data={**update_task_payload, "sub_tasks": []},
            context=context,
        )
        assert serializer.is_valid(), serializer.errors
        assert serializer.validated_data == {
            **validated_data_update,
            "sub_tasks": {"create_sub_tasks": [], "update_sub_tasks": []},
        }

    def test_update_existing_sub_task(
        self,
        sub_task: SubTask,
        context: Context,
        task: Task,
        update_task_payload: Any,
        validated_data_update: Any,
    ) -> None:
        """Test updating sub task."""
        title = "This is a new title, made for this sub task"
        payload = {"description": None, "done": True, "title": title}
        serializer = TaskUpdateSerializer(
            task,
            data={
                **update_task_payload,
                "sub_tasks": [{**payload, "uuid": str(sub_task.uuid)}],
            },
            context=context,
        )
        assert serializer.is_valid(), serializer.errors
        assert serializer.validated_data == {
            **validated_data_update,
            "sub_tasks": {
                "create_sub_tasks": [],
                "update_sub_tasks": [
                    {**payload, "_order": 0, "uuid": sub_task.uuid}
                ],
            },
        }

    def test_update_several_existing_sub_tasks(
        self,
        context: Context,
        task: Task,
        update_task_payload: Any,
        validated_data_update: Any,
        sub_tasks: list[SubTask],
    ) -> None:
        """Test updating several existing sub tasks."""
        title = "fancy factory fabricates fakes"
        payload = {"title": title, "done": False, "description": None}
        serializer = TaskUpdateSerializer(
            task,
            data={
                **update_task_payload,
                "sub_tasks": [
                    {**payload, "uuid": str(sub_task.uuid)}
                    for sub_task in sub_tasks
                ],
            },
            context=context,
        )
        assert serializer.is_valid(), serializer.errors
        assert serializer.validated_data == {
            **validated_data_update,
            "sub_tasks": {
                "create_sub_tasks": [],
                "update_sub_tasks": [
                    {**payload, "_order": 0, "uuid": sub_tasks[0].uuid},
                    {**payload, "_order": 1, "uuid": sub_tasks[1].uuid},
                    {**payload, "_order": 2, "uuid": sub_tasks[2].uuid},
                    {**payload, "_order": 3, "uuid": sub_tasks[3].uuid},
                    {**payload, "_order": 4, "uuid": sub_tasks[4].uuid},
                ],
            },
        }

    def test_update_one_create_one(
        self,
        context: Context,
        task: Task,
        update_task_payload: Any,
        validated_data_update: Any,
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
        serializer = TaskUpdateSerializer(
            task,
            data={
                **update_task_payload,
                "sub_tasks": [
                    # We change the order for some xtra spice
                    {"title": new_title, "done": False},
                    {
                        "uuid": str(sub_task.uuid),
                        "title": update_title,
                        "done": False,
                    },
                ],
            },
            context=context,
        )
        assert serializer.is_valid(), serializer.errors
        assert serializer.validated_data == {
            **validated_data_update,
            "sub_tasks": {
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
            },
        }

    def test_change_order(
        self,
        context: Context,
        task: Task,
        update_task_payload: Any,
        validated_data_update: Any,
        sub_tasks: list[SubTask],
    ) -> None:
        """Test changing the order of several sub tasks."""
        a, b, c, d, e = sub_tasks
        title = "asd"
        payload = {
            "title": title,
            "done": False,
            "description": None,
        }
        serializer = TaskUpdateSerializer(
            task,
            data={
                **update_task_payload,
                "sub_tasks": [
                    {**payload, "uuid": str(c.uuid)},
                    {**payload, "uuid": str(b.uuid)},
                    {**payload, "uuid": str(d.uuid)},
                    {**payload, "uuid": str(a.uuid)},
                    {**payload, "uuid": str(e.uuid)},
                ],
            },
            context=context,
        )
        assert serializer.is_valid(), serializer.errors
        assert serializer.validated_data == {
            **validated_data_update,
            "sub_tasks": {
                "create_sub_tasks": [],
                "update_sub_tasks": [
                    {**payload, "_order": 0, "uuid": c.uuid},
                    {**payload, "_order": 1, "uuid": b.uuid},
                    {**payload, "_order": 2, "uuid": d.uuid},
                    {**payload, "_order": 3, "uuid": a.uuid},
                    {**payload, "_order": 4, "uuid": e.uuid},
                ],
            },
        }

    def test_create_one_delete_one(
        self,
        context: Context,
        task: Task,
        sub_task: SubTask,
        update_task_payload: Any,
        validated_data_update: Any,
    ) -> None:
        """
        Test creating and deleting.

        1) The new sub task shall be created
        2) The missing sub task shall be deleted
        """
        title = "new sub task who dis"
        payload = {"title": title, "description": None, "done": False}
        assert task.subtask_set.get() == sub_task
        serializer = TaskUpdateSerializer(
            task,
            data={**update_task_payload, "sub_tasks": [payload]},
            context=context,
        )
        assert serializer.is_valid(), serializer.errors
        assert serializer.validated_data == {
            **validated_data_update,
            "sub_tasks": {
                "create_sub_tasks": [{**payload, "_order": 0}],
                "update_sub_tasks": [],
            },
        }

    def test_create_and_change_order(
        self,
        task: Task,
        context: Context,
        sub_tasks: list[SubTask],
        update_task_payload: Any,
        validated_data_update: Any,
    ) -> None:
        """
        Test creating sub tasks and changing the order of existing ones.

        1) The new tasks shall be inserted at the right place.
        2) Updated tasks shall be moved.
        """
        a, b, _, _, _ = sub_tasks
        title = "asd"
        new_title = "i am a new sub task"
        new_payload = {"description": None, "done": False, "title": new_title}
        update_payload = {"title": title, "description": None, "done": False}
        serializer = TaskUpdateSerializer(
            task,
            data={
                **update_task_payload,
                "sub_tasks": [
                    new_payload,
                    {"uuid": str(b.uuid), **update_payload},
                    new_payload,
                    {"uuid": str(a.uuid), **update_payload},
                ],
            },
            context=context,
        )
        assert serializer.is_valid(), serializer.errors
        assert serializer.validated_data == {
            **validated_data_update,
            "sub_tasks": {
                "create_sub_tasks": [
                    {**new_payload, "_order": 0},
                    {**new_payload, "_order": 2},
                ],
                "update_sub_tasks": [
                    {**update_payload, "_order": 1, "uuid": b.uuid},
                    {**update_payload, "_order": 3, "uuid": a.uuid},
                ],
            },
        }
