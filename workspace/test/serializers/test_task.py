"""Test workspace serializer."""
from unittest.mock import (
    MagicMock,
)
from uuid import uuid4

import pytest
from rest_framework.request import (
    Request,
)

from projectify.utils import validate_perm
from user.models import User
from workspace.models.label import Label
from workspace.models.sub_task import SubTask
from workspace.models.task import Task
from workspace.models.workspace import Workspace
from workspace.models.workspace_board_section import WorkspaceBoardSection
from workspace.models.workspace_user import WorkspaceUser
from workspace.services.workspace import (
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
        assert "number" not in serializer.validated_data
        assert "uuid" not in serializer.validated_data
        assert "title" in serializer.validated_data
        serializer.save()
        assert list(task.labels.values_list("uuid", flat=True)) == []
        assert task.assignee is None

        # Since we don't pass the sub task in, it will disappear
        assert list(SubTask.objects.all()) == []

    def test_create(
        self,
        label: Label,
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
        assert "title" in serializer.validated_data
        task = serializer.save()
        assert list(task.labels.values_list("uuid", flat=True)) == [label.uuid]
        assert task.assignee
        assert task.assignee.user.email == workspace_user.user.email

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
        workspace_board_section: WorkspaceBoardSection,
        sub_task: SubTask,
        user_request: Request,
    ) -> None:
        """Test updating a task."""
        assert len(task.subtask_set.all()) == 1
        serializer = serializers.TaskCreateUpdateSerializer(
            task,
            data={
                "title": task.title,
                "labels": [{"uuid": str(label.uuid)}],
                "assignee": {"uuid": str(workspace_user.uuid)},
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
        assert "title" in serializer.validated_data
        task = serializer.save()

        assert task.deadline is not None

        assert list(task.labels.values_list("uuid", flat=True)) == [label.uuid]

        assert task.assignee
        assert task.assignee.user.email == workspace_user.user.email

        sub_tasks = list(task.subtask_set.all())
        assert len(sub_tasks) == 3
        assert sub_tasks[1].uuid == sub_task.uuid
        assert sub_tasks[1].done == (not sub_task.done)

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
