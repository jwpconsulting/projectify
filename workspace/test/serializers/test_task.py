"""Test workspace serializer."""
from unittest.mock import (
    MagicMock,
)

from django.contrib.auth.models import (
    AbstractUser,
)

import pytest
from rest_framework.request import (
    Request,
)

from workspace.models.workspace_user import WorkspaceUser
from workspace.services.label import label_create
from workspace.services.workspace import (
    workspace_add_user,
)

from ... import (
    factory,
    models,
    serializers,
)


@pytest.mark.django_db
class TestTaskDetailSerializer:
    """Test the task detail serializer."""

    def test_readonly_fields(self, task: models.Task) -> None:
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
    def user_request(self, user: AbstractUser) -> Request:
        """Return a request with a user."""
        user_request = MagicMock()
        user_request.user = user
        return user_request

    def test_readonly_fields(
        self,
        task: models.Task,
        workspace_user: models.WorkspaceUser,
        workspace_board_section: models.WorkspaceBoardSection,
        sub_task: models.SubTask,
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
        assert list(models.SubTask.objects.all()) == []

    def test_create(
        self,
        label: models.Label,
        workspace_user: models.WorkspaceUser,
        workspace_board_section: models.WorkspaceBoardSection,
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
        workspace_user: models.WorkspaceUser,
        user_request: Request,
    ) -> None:
        """Test creating a task but the ws board section is wrong."""
        workspace_board_section = factory.WorkspaceBoardSectionFactory.create()
        serializer = serializers.TaskCreateUpdateSerializer(
            data={
                "title": "This is a great task title.",
                "labels": [],
                "assignee": None,
                "workspace_board_section": {
                    "uuid": str(workspace_board_section.uuid),
                },
            },
            context={"request": user_request},
        )
        assert not serializer.is_valid()
        assert serializer.errors["workspace_board_section"]

    def test_update(
        self,
        task: models.Task,
        label: models.Label,
        workspace_user: models.WorkspaceUser,
        workspace_board_section: models.WorkspaceBoardSection,
        sub_task: models.SubTask,
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
        task: models.Task,
        user_request: Request,
    ) -> None:
        """Test updating a task."""
        workspace_board_section = factory.WorkspaceBoardSectionFactory.create()
        serializer = serializers.TaskCreateUpdateSerializer(
            task,
            data={
                "title": task.title,
                "labels": [],
                "assignee": None,
                "workspace_board_section": {
                    "uuid": str(workspace_board_section.uuid),
                },
            },
            context={"request": user_request},
        )
        assert not serializer.is_valid()
        (error,) = serializer.errors["workspace_board_section"]
        assert "exist" in error

    def test_update_wrong_workspace(
        self,
        task: models.Task,
        workspace_user: models.WorkspaceUser,
        user_request: Request,
    ) -> None:
        """Test updating a task."""
        workspace_board_section = factory.WorkspaceBoardSectionFactory.create()
        workspace = workspace_board_section.workspace
        workspace_add_user(workspace, workspace_user.user)
        serializer = serializers.TaskCreateUpdateSerializer(
            task,
            data={
                "title": task.title,
                "labels": [],
                "assignee": None,
                "workspace_board_section": {
                    "uuid": str(workspace_board_section.uuid),
                },
            },
            context={"request": user_request},
        )
        assert not serializer.is_valid()
        (error,) = serializer.errors["workspace_board_section"]
        assert "cannot be assigned" in error

    def test_update_missing_label(
        self,
        task: models.Task,
        user_request: Request,
        label: models.Label,
        workspace_user: WorkspaceUser,
        other_workspace_workspace_user: WorkspaceUser,
    ) -> None:
        """Test updating a task."""
        other_label = label_create(
            workspace=other_workspace_workspace_user.workspace,
            who=other_workspace_workspace_user.user,
            color=0,
            name="don't care",
        )
        serializer = serializers.TaskCreateUpdateSerializer(
            task,
            data={
                "title": task.title,
                "labels": [
                    {"uuid": str(label.uuid)},
                    {"uuid": str(other_label.uuid)},
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
        task: models.Task,
        user_request: Request,
    ) -> None:
        """Test updating a task."""
        assignee = factory.WorkspaceUserFactory.create()
        serializer = serializers.TaskCreateUpdateSerializer(
            task,
            data={
                "title": task.title,
                "labels": [],
                "assignee": {"uuid": str(assignee.uuid)},
                "workspace_board_section": {
                    "uuid": str(task.workspace_board_section.uuid),
                },
            },
            context={"request": user_request},
        )
        assert not serializer.is_valid()
        (error,) = serializer.errors["assignee"]
        assert "could not be found" in error
