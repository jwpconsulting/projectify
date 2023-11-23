"""Task CRUD views."""
# Create
# Read
# Update
from typing import (
    Any,
    Union,
)
from uuid import UUID

from django.db.models import (
    Prefetch,
)
from django.shortcuts import get_object_or_404

from rest_framework import (
    generics,
    serializers,
    status,
)
from rest_framework.request import (
    Request,
)
from rest_framework.response import (
    Response,
)
from rest_framework.views import APIView

from workspace.models.task import Task
from workspace.serializers.task_detail import (
    TaskCreateUpdateSerializer,
    TaskDetailSerializer,
)
from workspace.services.task import task_move_after

from .. import (
    models,
)


class TaskCreate(
    generics.CreateAPIView[
        models.Task,
        models.TaskQuerySet,
        TaskCreateUpdateSerializer,
    ],
):
    """Create a task."""

    serializer_class = TaskCreateUpdateSerializer


class TaskRetrieveUpdateDestroy(
    generics.RetrieveUpdateDestroyAPIView[
        models.Task,
        models.TaskQuerySet,
        Union[
            TaskDetailSerializer,
            TaskCreateUpdateSerializer,
        ],
    ],
):
    """Retrieve a task."""

    objects = models.Task.objects
    queryset = (
        objects.select_related(
            "workspace_board_section__workspace_board__workspace",
            "assignee",
            "assignee__user",
        )
        .prefetch_related(
            "labels",
            "subtask_set",
        )
        .prefetch_related(
            Prefetch(
                "chatmessage_set",
                queryset=models.ChatMessage.objects.select_related(
                    "author",
                    "author__user",
                ),
            ),
        )
    )
    serializer_class = TaskDetailSerializer

    def get_object(self, full: bool = True) -> models.Task:
        """
        Get object for user and uuid.

        Without an additonal flag, we use the prefetch queryset. If full
        is passed in as false, we do not prefetch. This is useful for
        the update method.
        """
        user = self.request.user
        qs: models.TaskQuerySet
        if full:
            qs = self.get_queryset()
        else:
            qs = self.objects
        qs = qs.filter_for_user_and_uuid(
            user=user,
            uuid=self.kwargs["task_uuid"],
        )
        obj: models.Task = get_object_or_404(qs)
        return obj

    def update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Override update behavior. Return using different serializer.

        The idea is that we accept abbreviated nested fields, but return
        the data whole. (ws board section, sub tasks, labels, etc.)
        """
        # Copied from
        # https://github.com/encode/django-rest-framework/blob/d32346bae55f3e4718a185fb60e9f7a28e389c85/rest_framework/mixins.py#L65
        # We probably don't have to get the full object here!
        instance = self.get_object()
        serializer = TaskCreateUpdateSerializer(
            instance,
            data=request.data,
            # Mild code duplication from
            # https://github.com/encode/django-rest-framework/blob/d32346bae55f3e4718a185fb60e9f7a28e389c85/rest_framework/generics.py#L113
            # :)
            context=self.get_serializer_context(),
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        instance = self.get_object()
        response_serializer = self.serializer_class(instance)
        return Response(response_serializer.data)


# RPC
class TaskMove(APIView):
    """Move a task right behind another task."""

    class InputSerializer(serializers.Serializer):
        """Accept a task uuid after which this task should be moved."""

        after_task_uuid = serializers.UUIDField(allow_null=True)

    def post(self, request: Request, task_uuid: UUID) -> Response:
        """Process the request."""
        user = request.user
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        task_qs = Task.objects.filter_for_user_and_uuid(
            user=user,
            uuid=task_uuid,
        )
        task = get_object_or_404(
            task_qs,
        )
        after_task_uuid = data.get("after_task_uuid", None)
        if after_task_uuid is None:
            after_task = None
        else:
            after_task_qs = Task.objects.filter_for_user_and_uuid(
                user=user,
                uuid=data["after_task_uuid"],
            )
            try:
                after_task = after_task_qs.get()
            except Task.DoesNotExist:
                raise serializers.ValidationError(
                    {
                        "after_task_uuid": "Task with given uuid does not exist",
                    }
                )
        task_move_after(
            task=task,
            who=user,
            workspace_board_section=task.workspace_board_section,
            after=after_task,
        )

        task.refresh_from_db()
        output_serializer = TaskDetailSerializer(instance=task)
        return Response(output_serializer.data, status=status.HTTP_200_OK)
