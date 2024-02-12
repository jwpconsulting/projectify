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
"""Ensure unique Task number for current Task objects, part two."""
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


def add_unique_task_number(apps: Apps, schema_editor: object) -> None:
    """Add unique task number."""
    Task = cast("_Task", apps.get_model("workspace", "Task"))
    for task in Task.objects.all():
        if task.number is None:
            new_number = task.workspace.highest_task_number + 1
            task.number = new_number
            task.workspace.highest_task_number = new_number
            task.save()
            task.workspace.save()


class Migration(migrations.Migration):
    """Migration."""

    dependencies = [
        ("workspace", "0035"),
    ]

    operations = [
        migrations.RunPython(add_unique_task_number),
    ]
