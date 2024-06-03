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
from unittest.mock import (
    MagicMock,
)

import pytest
from rest_framework.request import (
    Request,
)

from projectify.user.models import User

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

pytestmark = pytest.mark.django_db


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


@pytest.fixture
def user_request(user: User) -> Request:
    """Return a request with a user."""
    user_request = MagicMock()
    user_request.user = user
    return user_request


class TestTaskCreateSerializer:
    """Test the task update serializer."""

    def test_readonly_fields(
        self,
        task: Task,
        workspace: Workspace,
        team_member: TeamMember,
        section: Section,
        sub_task: SubTask,
        user_request: Request,
    ) -> None:
        """Check that fields are actually readonly by trying a few."""
        assert task.subtask_set.count() == 1
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
            context={"request": user_request},
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
        user_request: Request,
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
            context={"request": user_request},
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
        team_member: TeamMember,
        user_request: Request,
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
            context={"request": user_request},
        )
        assert not serializer.is_valid()
        assert serializer.errors["section"]


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
        self,
        task: Task,
        user_request: Request,
        label: Label,
        team_member: TeamMember,
        unrelated_team_member: TeamMember,
        unrelated_label: Label,
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
            context={"request": user_request},
        )
        assert not serializer.is_valid(), serializer.validated_data
        assert "labels" in serializer.errors, serializer.errors
        (error,) = serializer.errors["labels"]
        assert "label could not be found" in error

    def test_update_wrong_assignee(
        self,
        task: Task,
        user_request: Request,
        unrelated_team_member: TeamMember,
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
            context={"request": user_request},
        )
        assert not serializer.is_valid()
        (error,) = serializer.errors["assignee"]
        assert "could not be found" in error
