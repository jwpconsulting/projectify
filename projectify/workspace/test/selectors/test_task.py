# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023 JWP Consulting GK
"""Test task selectors."""

import pytest

from projectify.user.models import User
from projectify.workspace.models.task import Task
from projectify.workspace.models.workspace import Workspace
from projectify.workspace.selectors.task import task_find_by_task_uuid
from pytest_types import DjangoAssertNumQueries


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
