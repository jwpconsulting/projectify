"""Task CRUD views."""
# Create
# Read
# Update
from django.db.models import (
    Prefetch,
)

from rest_framework import (
    generics,
)

from .. import (
    models,
    serializers,
)


class TaskRetrieveUpdate(
    generics.RetrieveUpdateAPIView[
        models.Task, models.TaskQuerySet, serializers.TaskDetailSerializer
    ],
):
    """Retrieve a task."""

    queryset = (
        models.Task.objects.select_related(
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

    def get_object(self) -> models.Task:
        """Get object for user and uuid."""
        user = self.request.user
        qs: models.TaskQuerySet = self.get_queryset()
        obj: models.Task = qs.filter_for_user_and_uuid(
            user,
            self.kwargs["task_uuid"],
        ).get()
        return obj
