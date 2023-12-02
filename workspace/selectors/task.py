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


def task_find_by_task_uuid(
    *, task_uuid: UUID, who: User, qs: Optional[TaskQuerySet] = None
) -> Optional[Task]:
    """Find a task given a user and uuid."""
    # Special care is needed, one can't write qs or Task.objects since that
    # would cause the given qs to be prematurely evaluated
    qs = Task.objects if qs is None else qs
    try:
        return qs.get(
            workspace_board_section__workspace_board__workspace__users=who,
            uuid=task_uuid,
        )
    except Task.DoesNotExist:
        return None
