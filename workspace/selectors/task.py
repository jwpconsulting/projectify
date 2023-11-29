"""Workspace selectors."""

from typing import Optional
from uuid import UUID

from user.models import User
from workspace.models.task import Task


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
