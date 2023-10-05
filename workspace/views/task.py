"""Task CRUD views."""
# Create
# Read
# Update
from typing import (
    Any,
    Union,
)

from django.db.models import (
    Prefetch,
)

from rest_framework import (
    generics,
)
from rest_framework.request import (
    Request,
)
from rest_framework.response import (
    Response,
)

from .. import (
    models,
    serializers,
)


class TaskCreate(
    generics.CreateAPIView[
        models.Task,
        models.TaskQuerySet,
        serializers.TaskCreateUpdateSerializer,
    ],
):
    """Create a task."""

    serializer_class = serializers.TaskCreateUpdateSerializer


class TaskRetrieveUpdate(
    generics.RetrieveUpdateAPIView[
        models.Task,
        models.TaskQuerySet,
        Union[
            serializers.TaskDetailSerializer,
            serializers.TaskCreateUpdateSerializer,
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
    serializer_class = serializers.TaskDetailSerializer

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
        obj: models.Task = generics.get_object_or_404(qs)
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
        serializer = serializers.TaskCreateUpdateSerializer(
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
