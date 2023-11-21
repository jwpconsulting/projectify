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
    from workspace.models import Task as _Task


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
