"""Test sub task model services."""
import pytest

from workspace.models.task import Task
from workspace.models.workspace_user import WorkspaceUser
from workspace.services.sub_task import sub_task_create


@pytest.mark.django_db
def test_add_sub_task(task: Task, workspace_user: WorkspaceUser) -> None:
    """Test adding a sub task."""
    assert task.subtask_set.count() == 0
    sub_task_create(
        who=workspace_user.user,
        task=task,
        title="don't care",
        done=False,
    )
    assert task.subtask_set.count() == 1
