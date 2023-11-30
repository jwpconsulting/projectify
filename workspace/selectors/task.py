"""Workspace selectors."""

from typing import Optional
from uuid import UUID

from django.db.models import Prefetch

from user.models import User
from workspace.models.chat_message import ChatMessage
from workspace.models.task import Task, TaskQuerySet

TaskDetailQuerySet: TaskQuerySet = (
    Task.objects.select_related(
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
            queryset=ChatMessage.objects.select_related(
                "author",
                "author__user",
            ),
        ),
    )
)


# TODO:
# Rename task_find_by_task_uuid
# Rename user to who
def find_task_for_user_and_uuid(
    *, task_uuid: UUID, user: User
) -> Optional[Task]:
    """Find a task given a user and uuid."""
    # TODO factor filter_for_user_and_uuid into here
    try:
        return Task.objects.filter_for_user_and_uuid(
            user=user, uuid=task_uuid
        ).get()
    except Task.DoesNotExist:
        return None
