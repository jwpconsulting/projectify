"""Test task selectors."""
import pytest

from pytest_types import DjangoAssertNumQueries
from user.models import User
from workspace.models.task import Task
from workspace.models.workspace import Workspace
from workspace.selectors.task import task_find_by_task_uuid


@pytest.mark.django_db
def test_task_find_by_task_uuid(
    workspace: Workspace,
    task: Task,
    user: User,
    meddling_user: User,
    django_assert_num_queries: DjangoAssertNumQueries,
) -> None:
    """Test filter_for_user_and_uuid."""
    with django_assert_num_queries(1):
        actual = task_find_by_task_uuid(
            who=user,
            task_uuid=task.uuid,
        )
    assert actual == task
    with django_assert_num_queries(1):
        assert (
            task_find_by_task_uuid(who=meddling_user, task_uuid=task.uuid)
            is None
        )
