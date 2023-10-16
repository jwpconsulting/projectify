"""Workspace signals."""
import logging
from collections.abc import (
    Mapping,
    Sequence,
)
from typing import (
    TYPE_CHECKING,
    Any,
    Type,
    TypeVar,
    Union,
    cast,
)

from django.db import models as django_models
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

from asgiref.sync import async_to_sync as _async_to_sync
from channels.layers import (
    get_channel_layer,
)
from rest_framework import serializers as drf_serializers

from user.signal_defs import (
    user_invitation_redeemed,
)

from . import (
    models,
    serializers,
    signal_defs,
    types,
)


if TYPE_CHECKING:
    from user.models import (  # noqa: F401
        User,
    )


Unknown = object


logger = logging.getLogger(__name__)

# TODO AsyncToSync is typed in a newer (unreleased) version of asgiref
# which we indirectly install with channels, which has not been
# renewed in a while Justus 2023-05-19
async_to_sync = cast(Any, _async_to_sync)


@receiver(signal_defs.workspace_user_invited)
def send_invitation_email(
    instance: models.WorkspaceUser, **kwargs: object
) -> None:
    """Send email when workspace user is invited."""
    # Avoid circular import
    from . import (
        emails,
    )

    email = emails.WorkspaceUserInviteEmail(instance)
    email.send()


def group_send(destination: str, message: types.Message) -> None:
    """Send message to a channels group."""
    channel_layer = get_channel_layer()
    if not channel_layer:
        raise Exception("Did not get channel layer")
    async_to_sync(channel_layer.group_send)(
        destination,
        message,
    )


M = TypeVar("M", bound=django_models.Model)


def serialize(
    serializer: Type[drf_serializers.ModelSerializer[M]],
    instance: M,
) -> Union[Mapping[str, Any], Sequence[Any]]:
    """Serialize a django model instance and then render it to JSON."""
    return serializer(instance).data


def send_workspace_change_signal(instance: models.Workspace) -> None:
    """Send workspace.change signal to correct group."""
    uuid = str(instance.uuid)
    data = serialize(serializers.WorkspaceDetailSerializer, instance)
    group_send(
        f"workspace-{uuid}",
        {
            "type": "workspace.change",
            "uuid": uuid,
            "data": data,
        },
    )


def send_workspace_board_change_signal(
    instance: models.WorkspaceBoard,
) -> None:
    """Send workspace_board.change signal to correct group."""
    uuid = str(instance.uuid)
    data = serialize(serializers.WorkspaceBoardDetailSerializer, instance)
    group_send(
        f"workspace-board-{uuid}",
        {
            "type": "workspace.board.change",
            "uuid": uuid,
            "data": data,
        },
    )


def send_task_change_signal(instance: models.Task) -> None:
    """Send task.change signal to correct group."""
    uuid = str(instance.uuid)
    data = serialize(serializers.TaskDetailSerializer, instance)
    group_send(
        f"task-{uuid}",
        {
            "type": "task.change",
            "uuid": uuid,
            "data": data,
        },
    )


@receiver(post_save, sender=models.Workspace)
@receiver(post_delete, sender=models.Workspace)
def workspace_changed(instance: models.Workspace, **kwargs: Unknown) -> None:
    """Broadcast changes upon workspace save/delete."""
    send_workspace_change_signal(instance)


@receiver(post_save, sender=models.Label)
@receiver(post_delete, sender=models.Label)
def label_changed(instance: models.Label, **kwargs: Unknown) -> None:
    """Broadcast changes upon label save/delete."""
    workspace = instance.workspace
    send_workspace_change_signal(workspace)


@receiver(post_save, sender=models.WorkspaceUser)
@receiver(post_delete, sender=models.WorkspaceUser)
def workspace_user_changed(
    instance: models.WorkspaceUser, **kwargs: Unknown
) -> None:
    """Broadcast changes upon workspace user save/delete."""
    workspace = instance.workspace
    send_workspace_change_signal(workspace)


@receiver(post_save, sender=models.WorkspaceBoard)
@receiver(post_delete, sender=models.WorkspaceBoard)
def workspace_board_changed(
    instance: models.WorkspaceBoard, **kwargs: Unknown
) -> None:
    """Broadcast changes upon workspace board save/delete."""
    send_workspace_board_change_signal(instance)
    send_workspace_change_signal(instance.workspace)


@receiver(post_save, sender=models.WorkspaceBoardSection)
@receiver(post_delete, sender=models.WorkspaceBoardSection)
def workspace_board_section_changed(
    instance: models.WorkspaceBoardSection, **kwargs: Unknown
) -> None:
    """Broadcast changes upon workspace board section save/delete."""
    workspace_board = instance.workspace_board
    send_workspace_board_change_signal(workspace_board)


@receiver(post_save, sender=models.Task)
@receiver(post_delete, sender=models.Task)
def task_changed(instance: models.Task, **kwargs: Unknown) -> None:
    """Broadcast changes upon task save/delete."""
    workspace_board = instance.workspace_board_section.workspace_board
    send_workspace_board_change_signal(workspace_board)
    send_task_change_signal(instance)


@receiver(post_save, sender=models.TaskLabel)
@receiver(post_delete, sender=models.TaskLabel)
def task_label_changed(instance: models.TaskLabel, **kwargs: Unknown) -> None:
    """Broadcast changes upon task label save/delete."""
    task = instance.task
    workspace_board = task.workspace_board_section.workspace_board
    send_workspace_board_change_signal(workspace_board)
    send_task_change_signal(task)


@receiver(post_save, sender=models.SubTask)
@receiver(post_delete, sender=models.SubTask)
def sub_task_changed(instance: models.SubTask, **kwargs: Unknown) -> None:
    """Broadcast changes upon sub task save/delete."""
    task = instance.task
    workspace_board = task.workspace_board_section.workspace_board
    send_workspace_board_change_signal(workspace_board)
    send_task_change_signal(task)


@receiver(post_save, sender=models.ChatMessage)
@receiver(post_delete, sender=models.ChatMessage)
def chat_message_changed(
    instance: models.ChatMessage, **kwargs: Unknown
) -> None:
    """Broadcast changes upon chat message save/delete."""
    task = instance.task
    send_task_change_signal(task)


@receiver(user_invitation_redeemed)
@transaction.atomic
def redeem_workspace_invitations(
    user: "User", instance: models.WorkspaceUserInvite, **kwargs: Unknown
) -> None:
    """Redeem workspace invitations."""
    qs = models.WorkspaceUserInvite.objects.filter(
        user_invite__user=user,
    )
    for invite in qs:
        invite.workspace.add_user(user)
        invite.redeem()
