"""Task services."""


from typing import Optional

from django.db import transaction

from projectify.utils import validate_perm
from user.models import User
from workspace.models.task import Task
from workspace.models.workspace_board_section import WorkspaceBoardSection


@transaction.atomic
def task_move_after(
    *,
    who: User,
    task: Task,
    after: Optional[Task],
    workspace_board_section: Optional[WorkspaceBoardSection],
) -> Task:
    """Move a task after another task. If no after is given, move to front."""
    validate_perm("workspace.can_update_task", who, task)
    # TODO this can be expressed more elegantly
    workspace_board_section = (
        workspace_board_section or task.workspace_board_section
    )
    if after is not None:
        order = after._order
    else:
        order = 0
    neighbor_tasks = task.workspace_board_section.task_set.select_for_update()
    # TODO this can be expressed more elegantly
    if task.workspace_board_section != workspace_board_section:
        other_tasks = workspace_board_section.task_set.select_for_update()
    else:
        # Same section, so no need to select other tasks
        other_tasks = None

    # Force both querysets to be evaluated to lock them for the time of
    # this transaction
    len(neighbor_tasks)
    # TODO this can be expressed more elegantly
    if other_tasks:
        len(other_tasks)
    # Set new WorkspaceBoardSection
    # TODO this can be expressed more elegantly
    if task.workspace_board_section != workspace_board_section:
        task.workspace_board_section = workspace_board_section
        task.save()

    # Change order
    order_list = list(workspace_board_section.get_task_order())
    current_object_index = order_list.index(task.pk)
    order_list.insert(order, order_list.pop(current_object_index))

    # Set the order
    workspace_board_section.set_task_order(order_list)
    workspace_board_section.save()
    return task
