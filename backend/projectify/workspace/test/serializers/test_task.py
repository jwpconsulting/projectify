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
from uuid import uuid4

import pytest
from rest_framework.request import (
    Request,
)

from projectify.lib.auth import validate_perm
from projectify.user.models import User
from projectify.workspace.models.label import Label
from projectify.workspace.models.sub_task import SubTask
from projectify.workspace.models.task import Task
from projectify.workspace.models.workspace import Workspace
from projectify.workspace.models.workspace_board_section import (
    WorkspaceBoardSection,
)
from projectify.workspace.models.workspace_user import WorkspaceUser
from projectify.workspace.services.workspace import (
    workspace_add_user,
)

from ... import (
    serializers,
)


@pytest.mark.django_db
class TestTaskDetailSerializer:
    """Test the task detail serializer."""

    def test_readonly_fields(self, task: Task) -> None:
        """Check that fields are actually readonly by trying a few."""
        serializer = serializers.TaskDetailSerializer(
            task,
            data={"title": task.title, "number": 133337, "uuid": 2},
        )
        # it is_valid, because DRF just ignores the read only fields inside
        # data
        serializer.is_valid(raise_exception=True)
        # Here we prove that DRF ignores "number" and other r/o fields
        assert "number" not in serializer.validated_data
        assert "uuid" not in serializer.validated_data
        assert "title" in serializer.validated_data


@pytest.mark.django_db
class TestTaskCreateUpdateSerializer:
    """Test the task update serializer."""

    @pytest.fixture
    def user_request(self, user: User) -> Request:
        """Return a request with a user."""
        user_request = MagicMock()
        user_request.user = user
        return user_request

    def test_readonly_fields(
        self,
        task: Task,
        workspace: Workspace,
        workspace_user: WorkspaceUser,
        workspace_board_section: WorkspaceBoardSection,
        sub_task: SubTask,
        user_request: Request,
    ) -> None:
        """Check that fields are actually readonly by trying a few."""
        assert task.subtask_set.count() == 1
        task.assign_to(workspace_user)
        serializer = serializers.TaskCreateUpdateSerializer(
            task,
            data={
                "title": task.title,
                "number": 133337,
                "uuid": 2,
                "labels": [],
                "assignee": None,
                "workspace_board_section": {
                    "uuid": str(workspace_board_section.uuid),
                },
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
            "workspace": workspace,
            "workspace_board_section": workspace_board_section,
        }

    def test_create(
        self,
        label: Label,
        workspace: Workspace,
        workspace_user: WorkspaceUser,
        workspace_board_section: WorkspaceBoardSection,
        user_request: Request,
    ) -> None:
        """Test creating a task."""
        serializer = serializers.TaskCreateUpdateSerializer(
            data={
                "title": "This is a great task title.",
                "labels": [{"uuid": str(label.uuid)}],
                "assignee": {"uuid": str(workspace_user.uuid)},
                "workspace_board_section": {
                    "uuid": str(workspace_board_section.uuid),
                },
            },
            context={"request": user_request},
        )
        serializer.is_valid(raise_exception=True)
        assert serializer.validated_data == {
            "assignee": workspace_user,
            "labels": [label],
            "title": "This is a great task title.",
            "workspace": workspace,
            "workspace_board_section": workspace_board_section,
        }

    def test_create_unrelated_workspace_board_section(
        self,
        workspace_user: WorkspaceUser,
        user_request: Request,
        unrelated_workspace_board_section: WorkspaceBoardSection,
    ) -> None:
        """Test creating a task but the ws board section is wrong."""
        serializer = serializers.TaskCreateUpdateSerializer(
            data={
                "title": "This is a great task title.",
                "labels": [],
                "assignee": None,
                "workspace_board_section": {
                    "uuid": str(unrelated_workspace_board_section.uuid),
                },
            },
            context={"request": user_request},
        )
        assert not serializer.is_valid()
        assert serializer.errors["workspace_board_section"]

    def test_update(
        self,
        task: Task,
        label: Label,
        workspace_user: WorkspaceUser,
        workspace: Workspace,
        workspace_board_section: WorkspaceBoardSection,
        sub_task: SubTask,
        user_request: Request,
    ) -> None:
        """Test updating a task."""
        assert len(task.subtask_set.all()) == 1
        assert task.due_date is not None
        due_date = task.due_date
        serializer = serializers.TaskCreateUpdateSerializer(
            task,
            data={
                "title": task.title,
                "labels": [{"uuid": str(label.uuid)}],
                "assignee": {"uuid": str(workspace_user.uuid)},
                "due_date": due_date.isoformat(),
                "workspace_board_section": {
                    "uuid": str(workspace_board_section.uuid),
                },
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
            "assignee": workspace_user,
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
            "workspace": workspace,
            "workspace_board_section": workspace_board_section,
        }

    def test_update_no_ws_board_section(
        self,
        task: Task,
        user_request: Request,
    ) -> None:
        """Test updating a task when a board does not exist."""
        serializer = serializers.TaskCreateUpdateSerializer(
            task,
            data={
                "title": task.title,
                "labels": [],
                "assignee": None,
                "workspace_board_section": {
                    "uuid": str(uuid4()),
                },
            },
            context={"request": user_request},
        )
        assert not serializer.is_valid()
        (error,) = serializer.errors["workspace_board_section"]
        assert "exist" in error

    def test_update_wrong_workspace(
        self,
        task: Task,
        workspace_user: WorkspaceUser,
        user_request: Request,
        unrelated_workspace_board_section: WorkspaceBoardSection,
        unrelated_workspace: Workspace,
    ) -> None:
        """Test assigning a task to an unrelated ws board section."""
        # We need to add ourselves to make sure we have access to the
        # workspace board section
        workspace_add_user(
            workspace=unrelated_workspace, user=workspace_user.user
        )
        # test for sanity
        validate_perm(
            "workspace.can_read_workspace_board_section",
            workspace_user.user,
            unrelated_workspace_board_section,
        )
        serializer = serializers.TaskCreateUpdateSerializer(
            task,
            data={
                "title": task.title,
                "labels": [],
                "assignee": None,
                "workspace_board_section": {
                    "uuid": str(unrelated_workspace_board_section.uuid),
                },
            },
            context={"request": user_request},
        )
        assert not serializer.is_valid()
        (error,) = serializer.errors["workspace_board_section"]
        assert "cannot be assigned" in error

    def test_update_missing_label(
        self,
        task: Task,
        user_request: Request,
        label: Label,
        workspace_user: WorkspaceUser,
        unrelated_workspace_user: WorkspaceUser,
        unrelated_label: Label,
    ) -> None:
        """Test updating with an unrelated label."""
        serializer = serializers.TaskCreateUpdateSerializer(
            task,
            data={
                "title": task.title,
                "labels": [
                    {"uuid": str(label.uuid)},
                    {"uuid": str(unrelated_label.uuid)},
                ],
                "assignee": None,
                "workspace_board_section": {
                    "uuid": str(task.workspace_board_section.uuid),
                },
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
        unrelated_workspace_user: WorkspaceUser,
    ) -> None:
        """Test updating a task."""
        serializer = serializers.TaskCreateUpdateSerializer(
            task,
            data={
                "title": task.title,
                "labels": [],
                "assignee": {"uuid": str(unrelated_workspace_user.uuid)},
                "workspace_board_section": {
                    "uuid": str(task.workspace_board_section.uuid),
                },
            },
            context={"request": user_request},
        )
        assert not serializer.is_valid()
        (error,) = serializer.errors["assignee"]
        assert "could not be found" in error
