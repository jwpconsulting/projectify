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
    from workspace.models import Task as _Task


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
