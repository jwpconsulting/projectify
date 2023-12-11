"""Task services."""
from datetime import datetime
from typing import Optional, Union

from django.db import transaction

from projectify.lib.auth import validate_perm
from user.models import User
from workspace.models.task import Task
from workspace.models.workspace_board_section import WorkspaceBoardSection
from workspace.models.workspace_user import WorkspaceUser


# Create
def task_create(
    *,
    who: User,
    workspace_board_section: WorkspaceBoardSection,
    title: str,
    description: Optional[str] = None,
    deadline: Optional[datetime] = None,
    assignee: Optional[WorkspaceUser] = None,
) -> "Task":
    """Add a task to this section."""
    validate_perm("workspace.can_create_task", who, workspace_board_section)
    # XXX Implicit N+1 here
    workspace = workspace_board_section.workspace_board.workspace
    return Task.objects.create(
        workspace_board_section=workspace_board_section,
        title=title,
        description=description,
        deadline=deadline,
        workspace=workspace,
        assignee=assignee,
    )


# Update
# Delete
def task_delete(*, task: Task, who: User) -> None:
    """Delete a task."""
    validate_perm("workspace.can_delete_task", who, task)
    task.delete()


@transaction.atomic
def task_move_after(
    *,
    who: User,
    task: Task,
    after: Union[Task, WorkspaceBoardSection],
) -> Task:
    """Move a task after a task or in front of a workspace board section."""
    validate_perm("workspace.can_update_task", who, task)
    match after:
        case Task():
            workspace_board_section = after.workspace_board_section
            order = after._order
        case WorkspaceBoardSection():
            workspace_board_section = after
            order = 0

    # Lock tasks in own workspace board section
    neighbor_tasks = workspace_board_section.task_set.select_for_update()
    len(neighbor_tasks)

    # Depending on whether we move within the same workspace board section, we
    # might have to lock only this workspace board section, or the destination
    # as well.
    if task.workspace_board_section != workspace_board_section:
        other_tasks = workspace_board_section.task_set.select_for_update()
        len(other_tasks)
        # And assign task's workspace board section
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
