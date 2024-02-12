# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Copyright (C) 2022, 2023 JWP Consulting GK
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
"""Ensure unique Task number for current Task objects."""
from typing import (
    TYPE_CHECKING,
    cast,
)

from django.apps.registry import (
    Apps,
)
from django.db import (
    migrations,
)

if TYPE_CHECKING:
    from projectify.workspace.models import Task as _Task


def add_workspace_to_task(apps: Apps, schema_editor: object) -> None:
    """Add unique task number."""
    Task = cast("_Task", apps.get_model("workspace", "Task"))
    for i, task in enumerate(Task.objects.all()):
        task.workspace = task.workspace_board_section.workspace_board.workspace
        task.save()


class Migration(migrations.Migration):
    """Migration."""

    dependencies = [
        ("workspace", "0034_task_number_task_workspace_and_more"),
    ]

    operations = [
        migrations.RunPython(add_workspace_to_task),
    ]
