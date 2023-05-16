"""Workspace signals."""
import logging

from django.db import (
    transaction,
)
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

from user.signal_defs import (
    user_invitation_redeemed,
)

from . import (
    models,
    signal_defs,
)


logger = logging.getLogger(__name__)


@receiver(signal_defs.workspace_user_invited)
def send_invitation_email(instance: models.WorkspaceUser, **kwargs):
    """Send email when workspace user is invited."""
    # Avoid circular import
    from . import (
        emails,
    )

    email = emails.WorkspaceUserInviteEmail(instance)
    email.send()


def send_workspace_change_signal(instance: models.Workspace):
    """Send workspace.change signal to correct group."""
    uuid = str(instance.uuid)
    channel_layer = get_channel_layer()
    if not channel_layer:
        raise Exception("Did not get channel layer")
    async_to_sync(channel_layer.group_send)(
        f"workspace-{uuid}",
        {
            "type": "workspace.change",
            "uuid": uuid,
        },
    )


def send_workspace_board_change_signal(instance: models.WorkspaceBoard):
    """Send workspace_board.change signal to correct group."""
    uuid = str(instance.uuid)
    channel_layer = get_channel_layer()
    if not channel_layer:
        raise Exception("Did not get channel layer")
    async_to_sync(channel_layer.group_send)(
        f"workspace-board-{uuid}",
        {
            "type": "workspace.board.change",
            "uuid": uuid,
        },
    )


def send_task_change_signal(instance: models.Task):
    """Send task.change signal to correct group."""
    uuid = str(instance.uuid)
    channel_layer = get_channel_layer()
    if not channel_layer:
        raise Exception("Did not get channel layer")
    async_to_sync(channel_layer.group_send)(
        f"task-{uuid}",
        {
            "type": "task.change",
            "uuid": uuid,
        },
    )


@receiver(post_save, sender=models.Workspace)
def workspace_saved(sender, instance: models.Workspace, **kwargs):
    """Broadcast changes."""
    send_workspace_change_signal(instance)


@receiver(post_delete, sender=models.Workspace)
def workspace_deleted(sender, instance: models.Workspace, **kwargs):
    """Broadcast changes upon workspace delete."""
    send_workspace_change_signal(instance)


@receiver(post_save, sender=models.Label)
def label_saved(sender, instance: models.Label, **kwargs):
    """Broadcast changes upon label save."""
    workspace = instance.workspace
    send_workspace_change_signal(workspace)


@receiver(post_delete, sender=models.Label)
def label_deleted(sender, instance: models.Label, **kwargs):
    """Broadcast changes upon label delete."""
    workspace = instance.workspace
    send_workspace_change_signal(workspace)


@receiver(post_save, sender=models.WorkspaceUser)
def workspace_user_saved(sender, instance: models.WorkspaceUser, **kwargs):
    """Broadcast changes."""
    workspace = instance.workspace
    send_workspace_change_signal(workspace)


@receiver(post_delete, sender=models.WorkspaceUser)
def workspace_user_delete(sender, instance: models.WorkspaceUser, **kwargs):
    """Broadcast changes."""
    workspace = instance.workspace
    send_workspace_change_signal(workspace)


@receiver(post_save, sender=models.WorkspaceBoard)
def workspace_board_saved(sender, instance: models.WorkspaceBoard, **kwargs):
    """Broadcast changes."""
    send_workspace_board_change_signal(instance)
    send_workspace_change_signal(instance.workspace)


@receiver(post_delete, sender=models.WorkspaceBoard)
def workspace_board_deleted(sender, instance: models.WorkspaceBoard, **kwargs):
    """Broadcast changes."""
    send_workspace_board_change_signal(instance)
    send_workspace_change_signal(instance.workspace)


@receiver(post_save, sender=models.WorkspaceBoardSection)
def workspace_board_section_saved(
    sender, instance: models.WorkspaceBoardSection, **kwargs
):
    """Broadcast changes."""
    workspace_board = instance.workspace_board
    send_workspace_board_change_signal(workspace_board)


@receiver(post_delete, sender=models.WorkspaceBoardSection)
def workspace_board_section_deleted(
    sender, instance: models.WorkspaceBoardSection, **kwargs
):
    """Broadcast changes."""
    workspace_board = instance.workspace_board
    send_workspace_board_change_signal(workspace_board)


@receiver(post_save, sender=models.Task)
def task_saved(sender, instance: models.Task, **kwargs):
    """Broadcast changes."""
    workspace_board = instance.workspace_board_section.workspace_board
    send_workspace_board_change_signal(workspace_board)
    send_task_change_signal(instance)


@receiver(post_delete, sender=models.Task)
def task_deleted(sender, instance: models.Task, **kwargs):
    """Broadcast changes."""
    workspace_board = instance.workspace_board_section.workspace_board
    send_workspace_board_change_signal(workspace_board)
    send_task_change_signal(instance)


@receiver(post_save, sender=models.TaskLabel)
def task_label_saved(sender, instance: models.TaskLabel, **kwargs):
    """Broadcast changes upon task label save."""
    task = instance.task
    workspace_board = task.workspace_board_section.workspace_board
    send_workspace_board_change_signal(workspace_board)
    send_task_change_signal(task)


@receiver(post_delete, sender=models.TaskLabel)
def task_label_deleted(sender, instance: models.TaskLabel, **kwargs):
    """Broadcast changes upon task label delete."""
    task = instance.task
    workspace_board = task.workspace_board_section.workspace_board
    send_workspace_board_change_signal(workspace_board)
    send_task_change_signal(task)


@receiver(post_save, sender=models.SubTask)
def sub_task_saved(sender, instance: models.SubTask, **kwargs):
    """Broadcast changes."""
    task = instance.task
    workspace_board = task.workspace_board_section.workspace_board
    send_workspace_board_change_signal(workspace_board)
    send_task_change_signal(task)


@receiver(post_delete, sender=models.SubTask)
def sub_task_deleted(sender, instance: models.SubTask, **kwargs):
    """Broadcast changes."""
    task = instance.task
    workspace_board = task.workspace_board_section.workspace_board
    send_workspace_board_change_signal(workspace_board)
    send_task_change_signal(task)


@receiver(post_save, sender=models.ChatMessage)
def chat_message_saved(sender, instance: models.ChatMessage, **kwargs):
    """Broadcast changes."""
    task = instance.task
    send_task_change_signal(task)


@receiver(post_delete, sender=models.ChatMessage)
def chat_message_deleted(sender, instance: models.ChatMessage, **kwargs):
    """Broadcast changes."""
    task = instance.task
    send_task_change_signal(task)


@receiver(user_invitation_redeemed)
@transaction.atomic
def redeem_workspace_invitations(
    user, instance: models.WorkspaceUserInvite, **kwargs
):
    """Redeem workspace invitations."""
    qs = models.WorkspaceUserInvite.objects.filter(
        user_invite__user=user,
    )
    for invite in qs:
        invite.workspace.add_user(user)
        invite.redeem()
