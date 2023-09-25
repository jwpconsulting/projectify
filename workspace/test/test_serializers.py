"""Test workspace serializer."""
import pytest

from .. import (
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

    def test_readonly_fields(self, task: models.Task) -> None:
        """Check that fields are actually readonly by trying a few."""
        serializer = serializers.TaskUpdateSerializer(
            task,
            data={
                "title": task.title,
                "number": 133337,
                "uuid": 2,
                "labels": [],
                "assignee": None,
            },
        )
        # it is_valid, because DRF just ignores the read only fields inside
        # data
        serializer.is_valid(raise_exception=True)
        # Here we prove that DRF ignores "number" and other r/o fields
        assert "number" not in serializer.validated_data
        assert "uuid" not in serializer.validated_data
        assert "title" in serializer.validated_data

    def test_assigning_label(
        self, task: models.Task, label: models.Label
    ) -> None:
        """Check that fields are actually readonly by trying a few."""
        # TODO try assigning one more
        label_uuids = [label.uuid]
        serializer = serializers.TaskUpdateSerializer(
            task,
            data={
                "title": task.title,
                "number": 133337,
                "uuid": 2,
                "labels": label_uuids,
                "assignee": None,
            },
        )
        # it is_valid, because DRF just ignores the read only fields inside
        # data
        serializer.is_valid(raise_exception=True)
        # Here we prove that DRF ignores "number" and other r/o fields
        assert "number" not in serializer.validated_data
        assert "uuid" not in serializer.validated_data
        assert "title" in serializer.validated_data
        serializer.save()
        assert list(task.labels.values_list("uuid", flat=True)) == label_uuids
