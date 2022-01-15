"""Workspace signals."""
from django.db.models.signals import (
    post_save,
)
from django.dispatch import (
    receiver,
)

from . import (
    models,
    schema,
)


@receiver(post_save, sender=models.WorkspaceBoard)
def workspace_board_saved(sender, instance, **kwargs):
    """Broadcast changes."""
    schema.OnWorkspaceBoardChange.broadcast(
        group=str(instance.uuid),
        payload=instance,
    )


@receiver(post_save, sender=models.WorkspaceBoardSection)
def workspace_board_section_saved(sender, instance, **kwargs):
    """Broadcast changes."""
    schema.OnWorkspaceBoardChange.broadcast(
        group=str(instance.workspace_board.uuid),
        payload=instance.workspace_board,
    )


@receiver(post_save, sender=models.Task)
def task_saved(sender, instance, **kwargs):
    """Broadcast changes."""
    schema.OnWorkspaceBoardChange.broadcast(
        group=str(instance.workspace_board_section.workspace_board.uuid),
        payload=instance.workspace_board_section.workspace_board,
    )


@receiver(post_save, sender=models.SubTask)
def sub_task_aveed(sender, instance, **kwargs):
    """Broadcast changes."""
    schema.OnWorkspaceBoardChange.broadcast(
        group=str(instance.task.workspace_board_section.workspace_board.uuid),
        payload=instance.task.workspace_board_section.workspace_board,
    )
