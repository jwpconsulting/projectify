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
class TestTaskUpdateSerializer:
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
        user_request: Request,
    ) -> None:
        """Check that fields are actually readonly by trying a few."""
        task.assign_to(workspace_user)
        serializer = serializers.TaskCreateUpdateSerializer(
            task,
            data={
                "title": task.title,
                "number": 133337,
                "uuid": 2,
                "labels": [],
                "assignee": None,
                "workspace_board_section": workspace_board_section.uuid,
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

    def test_create(
        self,
        label: models.Label,
        workspace_user: models.WorkspaceUser,
        workspace_board_section: models.WorkspaceBoardSection,
        user_request: Request,
    ) -> None:
        """Test creating a task."""
        label_uuids = [label.uuid]
        serializer = serializers.TaskCreateUpdateSerializer(
            data={
                "title": "This is a great task title.",
                "labels": label_uuids,
                "assignee": workspace_user.uuid,
                "workspace_board_section": workspace_board_section.uuid,
            },
            context={"request": user_request},
        )
        serializer.is_valid(raise_exception=True)
        assert "title" in serializer.validated_data
        task = serializer.save()
        assert list(task.labels.values_list("uuid", flat=True)) == label_uuids
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
                "workspace_board_section": workspace_board_section.uuid,
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
        user_request: Request,
    ) -> None:
        """Test updating a task."""
        # TODO try assigning one more
        label_uuids = [label.uuid]
        serializer = serializers.TaskCreateUpdateSerializer(
            task,
            data={
                "title": task.title,
                "labels": label_uuids,
                "assignee": workspace_user.uuid,
                "workspace_board_section": workspace_board_section.uuid,
            },
            context={"request": user_request},
        )
        serializer.is_valid(raise_exception=True)
        assert "title" in serializer.validated_data
        serializer.save()
        assert list(task.labels.values_list("uuid", flat=True)) == label_uuids
        assert task.deadline is not None
        assert task.assignee
        assert task.assignee.user.email == workspace_user.user.email

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
                "workspace_board_section": workspace_board_section.uuid,
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
        workspace.add_user(workspace_user.user)
        serializer = serializers.TaskCreateUpdateSerializer(
            task,
            data={
                "title": task.title,
                "labels": [],
                "assignee": None,
                "workspace_board_section": workspace_board_section.uuid,
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
    ) -> None:
        """Test updating a task."""
        other_label = factory.LabelFactory.create()
        serializer = serializers.TaskCreateUpdateSerializer(
            task,
            data={
                "title": task.title,
                "labels": [label.uuid, other_label.uuid],
                "assignee": None,
                "workspace_board_section": task.workspace_board_section.uuid,
            },
            context={"request": user_request},
        )
        assert not serializer.is_valid()
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
                "assignee": assignee.uuid,
                "workspace_board_section": task.workspace_board_section.uuid,
            },
            context={"request": user_request},
        )
        assert not serializer.is_valid()
        (error,) = serializer.errors["assignee"]
        assert "could not be found" in error