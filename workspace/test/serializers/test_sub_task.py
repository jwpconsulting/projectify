"""Test sub task serializers."""
from typing import (
    Any,
    Union,
)
from uuid import (
    UUID,
)

import pytest

from ...factory import (
    SubTaskFactory,
)
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
def context(task: Task) -> Context:
    """Return serializer context."""
    return {"task": task}


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
                "done": False,
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
        serializer.save()
        assert SubTask.objects.count() == 1
        new_sub_task = SubTask.objects.get()
        assert new_sub_task.title == payload_single["title"]
        assert new_sub_task.done == payload_single["done"]

    def test_create_no_context(
        self,
        payload_single: PayloadSingle,
        task: Task,
    ) -> None:
        """Test that without a context, we can still pass in the task."""
        assert SubTask.objects.count() == 0
        serializer = SubTaskCreateUpdateSerializer(
            data=[payload_single],
            many=True,
        )
        assert serializer.is_valid()
        serializer.create(serializer.validated_data, task)
        assert SubTask.objects.count() == 1

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
        serializer.save()
        assert SubTask.objects.count() == n

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
        serializer.save()
        assert SubTask.objects.count() == 0, SubTask.objects.all()

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
        serializer.save()
        assert SubTask.objects.count() == 1
        sub_task.refresh_from_db()
        assert sub_task.title == new_title

    def test_update_several_existing_sub_tasks(
        self, task: Task, context: Context
    ) -> None:
        """Test updating several existing sub tasks."""
        N = 5
        sub_tasks = SubTaskFactory.create_batch(N, task=task)
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
        serializer.save()
        assert SubTask.objects.count() == N
        for sub_task in task.subtask_set.all():
            assert sub_task.title == new_title

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
        serializer.save()
        assert task.subtask_set.count() == 2
        a, b = task.subtask_set.all()
        assert a.title == new_title
        assert b.title == update_title

    def test_change_order(self, task: Task, context: Context) -> None:
        """Test changing the order of several sub tasks."""
        N = 5
        a, b, c, d, e = SubTaskFactory.create_batch(N, task=task)
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
        serializer.save()
        assert SubTask.objects.count() == N
        new_order: list[UUID] = list(
            task.subtask_set.values_list("uuid", flat=True)
        )
        assert new_order == [c.uuid, b.uuid, d.uuid, a.uuid, e.uuid]

    def test_create_one_delete_one(
        self, task: Task, context: Context, sub_task: SubTask
    ) -> None:
        """
        Test creating and deleting.

        1) The new sub task shall be created
        2) The missing sub task shall be deleted
        """
        assert task.subtask_set.count() == 1
        serializer = SubTaskCreateUpdateSerializer(
            None,
            data=[
                {"title": "new sub task who dis", "done": False},
            ],
            many=True,
            context=context,
        )
        assert serializer.is_valid(), serializer.errors
        serializer.save()
        assert task.subtask_set.count() == 1
        new_sub_task = task.subtask_set.get()
        assert new_sub_task.title == "new sub task who dis"
        assert new_sub_task.uuid != sub_task.uuid

    def test_create_and_change_order(
        self, task: Task, context: Context
    ) -> None:
        """
        Test creating sub tasks and changing the order of existing ones.

        1) The new tasks shall be inserted at the right place.
        2) Updated tasks shall be moved.
        """
        a, b = SubTaskFactory.create_batch(2, task=task)
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
        serializer.save()
        assert SubTask.objects.count() == 4
        new_order: list[UUID] = list(
            task.subtask_set.values_list("uuid", flat=True)
        )
        assert new_order[1] == b.uuid, new_order
        assert new_order[3] == a.uuid, new_order


@pytest.mark.django_db
class TestSubTaskCreateUpdateSerializer:
    """Test SubTaskCreateUpdateSerializer."""

    # Serialize single existing
    def test_existing_subtask(self, sub_task: SubTask) -> None:
        """Test that nothing exciting happens when passing in an empty list."""
        serializer = SubTaskCreateUpdateSerializer(sub_task)
        assert serializer.data == {
            "uuid": str(sub_task.uuid),
            "title": sub_task.title,
            "description": sub_task.description,
            "done": False,
        }

    def test_new_sub_task(
        self,
        payload_single: PayloadSingle,
        context: Context,
    ) -> None:
        """Test we can create a new sub task."""
        serializer = SubTaskCreateUpdateSerializer(
            data=payload_single, context=context
        )
        assert serializer.is_valid(), serializer.errors
        serializer.save()
        assert SubTask.objects.count() == 1

    def test_new_sub_task_no_context(
        self,
        payload_single: PayloadSingle,
        task: Task,
    ) -> None:
        """Test we can create a new sub task even with no context."""
        serializer = SubTaskCreateUpdateSerializer(data=payload_single)
        assert serializer.is_valid(), serializer.errors
        validated_data = serializer.validated_data
        serializer.create(validated_data, task)
        assert SubTask.objects.count() == 1

    def test_update_sub_task(
        self,
        sub_task: SubTask,
        payload_single: PayloadSingle,
    ) -> None:
        """Test we can update an existing sub task."""
        serializer = SubTaskCreateUpdateSerializer(
            sub_task,
            data={**payload_single, "uuid": str(sub_task.uuid)},
        )
        assert serializer.is_valid(), serializer.errors
        serializer.save()
        assert SubTask.objects.count() == 1
        sub_task.refresh_from_db()
        assert sub_task.title == payload_single["title"]
        assert sub_task.done == payload_single["done"]
