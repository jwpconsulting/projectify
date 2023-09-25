"""
Task detail serializer.

We have put this here to avoid circular reference problems,
because ws board section requires importing the task serializer.
"""
from typing import (
    Any,
    Callable,
)

from django.contrib.auth import (
    get_user_model,
)
from django.contrib.auth.models import (
    AbstractBaseUser,
)

from rest_framework import (
    serializers,
)

from workspace.serializers.task import (
    TaskWithSubTaskSerializer,
)
from workspace.serializers.workspace_board_section import (
    WorkspaceBoardSectionUpSerializer,
)

from .. import (
    models,
)
from . import (
    base,
)


class TaskDetailSerializer(TaskWithSubTaskSerializer):
    """
    Serialize all task details.

    Serializes up to the workspace in one direction, and all chat messages,
    labels and sub task in the other direction.
    """

    chat_messages = base.ChatMessageBaseSerializer(
        many=True, read_only=True, source="chatmessage_set"
    )
    workspace_board_section = WorkspaceBoardSectionUpSerializer(read_only=True)

    class Meta(TaskWithSubTaskSerializer.Meta):
        """Meta."""

        fields = (
            *TaskWithSubTaskSerializer.Meta.fields,
            "chat_messages",
            "workspace_board_section",
        )


class TaskUpdateSerializer(base.TaskBaseSerializer):
    """
    Serialize update information for a task.

    Instead of serializing label and assignee, it accepts label uuids and
    assignee uuid and evaluates them.
    """

    labels = serializers.ListField(
        child=serializers.UUIDField(),
        write_only=True,
    )
    assignee = serializers.EmailField(
        allow_null=True,
        write_only=True,
    )

    def update(
        self, instance: models.Task, validated_data: dict[str, Any]
    ) -> models.Task:
        """Assign labels, assign assignee."""
        # Assign label
        label_uuids = validated_data.pop("labels")
        workspace_user_email = validated_data.pop("assignee")
        task = super().update(instance, validated_data)

        # Restrict to this workspace's labels
        # Wrong uuids are quietly ignored, don't know if that's great.
        labels = task.workspace.label_set.filter(uuid__in=label_uuids)
        task.set_labels(list(labels))
        # Assign ws user
        # get_by_natural_key is right here
        # https://github.com/django/django/blob/2128a73713735fb794ca6565fd5d7792293f5cfa/django/contrib/auth/base_user.py#L20
        if workspace_user_email:
            get_by_natural_key: Callable[
                [str], AbstractBaseUser
            ] = get_user_model().objects.get_by_natural_key  # type: ignore[attr-defined]
            user: AbstractBaseUser = get_by_natural_key(workspace_user_email)
            workspace_user = task.workspace.workspaceuser_set.get(user=user)
            task.assign_to(workspace_user)
        return task
