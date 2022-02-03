"""Workspace signals."""
from django.db.models.signals import (
    post_save,
)
from django.dispatch import (
    receiver,
)

from asgiref.sync import (
    async_to_sync,
)
from channels.layers import (
    get_channel_layer,
)

from . import (
    models,
)
from .schema import (
    subscription,
)


@receiver(post_save, sender=models.WorkspaceBoard)
def workspace_board_saved(sender, instance, **kwargs):
    """Broadcast changes."""
    uuid = str(instance.uuid)
    subscription.OnWorkspaceBoardChange.broadcast(
        group=uuid,
        payload=instance,
    )
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"workspace-board-{uuid}",
        {
            "type": "workspace.board.change",
            "instance": instance,
        },
    )


@receiver(post_save, sender=models.WorkspaceBoardSection)
def workspace_board_section_saved(sender, instance, **kwargs):
    """Broadcast changes."""
    workspace_board = instance.workspace_board
    uuid = str(workspace_board.uuid)
    subscription.OnWorkspaceBoardChange.broadcast(
        group=uuid,
        payload=workspace_board,
    )
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"workspace-board-{uuid}",
        {
            "type": "workspace.board.change",
            "instance": workspace_board,
        },
    )


@receiver(post_save, sender=models.Task)
def task_saved(sender, instance, **kwargs):
    """Broadcast changes."""
    workspace_board = instance.workspace_board_section.workspace_board
    uuid = str(workspace_board.uuid)
    subscription.OnWorkspaceBoardChange.broadcast(
        group=uuid,
        payload=workspace_board,
    )
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"workspace-board-{uuid}",
        {
            "type": "workspace.board.change",
            "instance": workspace_board,
        },
    )


@receiver(post_save, sender=models.SubTask)
def sub_task_saved(sender, instance, **kwargs):
    """Broadcast changes."""
    workspace_board = instance.task.workspace_board_section.workspace_board
    uuid = str(workspace_board.uuid)
    subscription.OnWorkspaceBoardChange.broadcast(
        group=uuid,
        payload=workspace_board,
    )
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"workspace-board-{uuid}",
        {
            "type": "workspace.board.change",
            "instance": workspace_board,
        },
    )
