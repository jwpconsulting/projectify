"""Workspace signals."""
from django.db.models.signals import (
    post_delete,
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


@receiver(post_save, sender=models.Workspace)
def workspace_saved(sender, instance, **kwargs):
    """Broadcast changes."""
    uuid = str(instance.uuid)
    subscription.OnWorkspaceChange.broadcast(
        group=uuid,
        payload=instance,
    )
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"workspace-{uuid}",
        {
            "type": "workspace.change",
            "uuid": uuid,
        },
    )


@receiver(post_save, sender=models.WorkspaceUser)
def workspace_user_saved(sender, instance, **kwargs):
    """Broadcast changes."""
    uuid = str(instance.workspace.uuid)
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"workspace-{uuid}",
        {
            "type": "workspace.change",
            "uuid": uuid,
        },
    )


@receiver(post_delete, sender=models.WorkspaceUser)
def workspace_user_delete(sender, instance, **kwargs):
    """Broadcast changes."""
    uuid = str(instance.workspace.uuid)
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"workspace-{uuid}",
        {
            "type": "workspace.change",
            "uuid": uuid,
        },
    )


@receiver(post_save, sender=models.WorkspaceBoard)
def workspace_board_saved(sender, instance, **kwargs):
    """Broadcast changes."""
    uuid = str(instance.uuid)
    workspace_uuid = str(instance.workspace.uuid)
    subscription.OnWorkspaceBoardChange.broadcast(
        group=uuid,
        payload=instance,
    )
    subscription.OnWorkspaceChange.broadcast(
        group=str(instance.workspace.uuid),
        payload=instance.workspace,
    )
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"workspace-board-{uuid}",
        {
            "type": "workspace.board.change",
            "uuid": uuid,
        },
    )
    async_to_sync(channel_layer.group_send)(
        f"workspace-{uuid}",
        {
            "type": "workspace.change",
            "uuid": workspace_uuid,
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
            "uuid": uuid,
        },
    )


@receiver(post_save, sender=models.Task)
def task_saved(sender, instance, **kwargs):
    """Broadcast changes."""
    workspace_board = instance.workspace_board_section.workspace_board
    uuid = str(workspace_board.uuid)
    task_uuid = str(instance.uuid)
    subscription.OnWorkspaceBoardChange.broadcast(
        group=uuid,
        payload=workspace_board,
    )
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"workspace-board-{uuid}",
        {
            "type": "workspace.board.change",
            "uuid": uuid,
        },
    )
    async_to_sync(channel_layer.group_send)(
        f"task-{task_uuid}",
        {
            "type": "task.change",
            "uuid": task_uuid,
        },
    )


@receiver(post_delete, sender=models.Task)
def task_deleted(sender, instance, **kwargs):
    """Broadcast changes."""
    task_uuid = str(instance.uuid)
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"task-{task_uuid}",
        {
            "type": "task.change",
            "uuid": task_uuid,
        },
    )


@receiver(post_save, sender=models.SubTask)
def sub_task_saved(sender, instance, **kwargs):
    """Broadcast changes."""
    workspace_board = instance.task.workspace_board_section.workspace_board
    uuid = str(workspace_board.uuid)
    task_uuid = str(instance.task.uuid)
    subscription.OnWorkspaceBoardChange.broadcast(
        group=uuid,
        payload=workspace_board,
    )
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"workspace-board-{uuid}",
        {
            "type": "workspace.board.change",
            "uuid": uuid,
        },
    )
    async_to_sync(channel_layer.group_send)(
        f"task-{task_uuid}",
        {
            "type": "task.change",
            "uuid": task_uuid,
        },
    )


@receiver(post_delete, sender=models.SubTask)
def sub_task_deleted(sender, instance, **kwargs):
    """Broadcast changes."""
    task_uuid = str(instance.task.uuid)
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"task-{task_uuid}",
        {
            "type": "task.change",
            "uuid": task_uuid,
        },
    )


@receiver(post_save, sender=models.ChatMessage)
def chat_message_saved(sender, instance, **kwargs):
    """Broadcast changes."""
    uuid = str(instance.task.uuid)
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"task-{uuid}",
        {
            "type": "task.change",
            "uuid": uuid,
        },
    )


@receiver(post_delete, sender=models.ChatMessage)
def chat_message_deleted(sender, instance, **kwargs):
    """Broadcast changes."""
    uuid = str(instance.task.uuid)
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"task-{uuid}",
        {
            "type": "task.change",
            "uuid": uuid,
        },
    )


@receiver(post_delete, sender=models.WorkspaceBoard)
def workspace_board_deleted(sender, instance, **kwargs):
    """Broadcast changes."""
    uuid = str(instance.uuid)
    workspace_uuid = str(instance.workspace.uuid)
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"workspace-board-{uuid}",
        {
            "type": "workspace.board.change",
            "uuid": uuid,
        },
    )
    async_to_sync(channel_layer.group_send)(
        f"workspace-{uuid}",
        {
            "type": "workspace.change",
            "uuid": workspace_uuid,
        },
    )


@receiver(post_delete, sender=models.WorkspaceBoardSection)
def workspace_board_section_deleted(sender, instance, **kwargs):
    """Broadcast changes."""
    uuid = str(instance.workspace_board.uuid)
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"workspace-board-{uuid}",
        {
            "type": "workspace.board.change",
            "uuid": uuid,
        },
    )


@receiver(post_delete, sender=models.Task)
def workspace_task_deleted(sender, instance, **kwargs):
    """Broadcast changes."""
    uuid = str(instance.workspace_board_section.workspace_board.uuid)
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"workspace-board-{uuid}",
        {
            "type": "workspace.board.change",
            "uuid": uuid,
        },
    )


@receiver(post_delete, sender=models.SubTask)
def workspace_sub_task_deleted(sender, instance, **kwargs):
    """Broadcast changes."""
    uuid = str(instance.task.workspace_board_section.workspace_board.uuid)
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"workspace-board-{uuid}",
        {
            "type": "workspace.board.change",
            "uuid": uuid,
        },
    )
