"""Sub task services."""
from typing import Optional

from projectify.utils import validate_perm
from user.models import User
from workspace.models.sub_task import SubTask
from workspace.models.task import Task


def sub_task_create(
    *,
    who: User,
    task: Task,
    title: str,
    done: bool,
    description: Optional[str] = None,
) -> SubTask:
    """Create a sub task for a task."""
    validate_perm("workspace.can_create_sub_task", who, task)
    return SubTask.objects.create(
        task=task, title=title, description=description, done=done
    )
