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
