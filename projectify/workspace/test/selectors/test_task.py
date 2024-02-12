# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Copyright (C) 2023 JWP Consulting GK
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
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
