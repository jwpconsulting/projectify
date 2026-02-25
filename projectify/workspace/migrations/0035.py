# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2022, 2023 JWP Consulting GK
"""Ensure unique Task number for current Task objects."""

from typing import Any, cast

from django.apps.registry import Apps
from django.db import migrations


def add_workspace_to_task(apps: Apps, schema_editor: object) -> None:
    """Add unique task number."""
    Task = cast(Any, apps.get_model("workspace", "Task"))
    for _, task in enumerate(Task.objects.all()):
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
