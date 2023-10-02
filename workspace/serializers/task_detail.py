"""
Task detail serializer.

We have put this here to avoid circular reference problems,
because ws board section requires importing the task serializer.
"""
from typing import (
    Any,
    Optional,
)
from uuid import (
    UUID,
)

from django.contrib.auth.models import (
    AbstractBaseUser,
)
from django.db import (
    transaction,
)
from django.utils.translation import gettext_lazy as _

from rest_framework import (
    serializers,
)
from rest_framework.request import (
    Request,
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


def assign_labels(task: models.Task, labels: list[models.Label]) -> None:
    """Assign label uuids to the given task."""
    task.set_labels(labels)


# Make me TaskCreateUpdateSerializer
class TaskCreateUpdateSerializer(base.TaskBaseSerializer):
    """
    Serialize update information for a task.

    Instead of serializing label and assignee, it accepts label uuids and
    assignee uuid and evaluates them.
    """

    workspace_board_section = serializers.UUIDField(
        write_only=True,
    )
    # TODO make label optional, when unset keep previous or on create
    # do not assign
    labels = serializers.ListField(
        child=serializers.UUIDField(),
        write_only=True,
    )
    # TODO make assignee optional
    # When unset, keep previous value or on create do not assign
    assignee = serializers.UUIDField(
        allow_null=True,
        write_only=True,
    )

    def validate_workspace_board_section(
        self, value: UUID
    ) -> models.WorkspaceBoardSection:
        """Validate the workspace board section."""
        request: Request = self.context["request"]
        user: AbstractBaseUser = request.user

        # First, we make sure we are assigning the task to a workspace board
        # section that the request's user has access to.
        try:
            workspace_board_section = (
                models.WorkspaceBoardSection.objects.filter_for_user_and_uuid(
                    user=user,
                    uuid=value,
                ).get()
            )
        except models.WorkspaceBoardSection.DoesNotExist:
            raise serializers.ValidationError(
                _("Workspace board section does not exist"),
            )
        workspace: models.Workspace = workspace_board_section.workspace
        if self.instance and self.instance.workspace != workspace:
            raise serializers.ValidationError(
                _("This task cannot be assigned to another workspace"),
            )
        return workspace_board_section

    def validate(self, data: dict[str, Any]) -> dict[str, Any]:
        """Validate user access to ws board sect, assignee and labels."""
        workspace_board_section: models.WorkspaceBoardSection = data[
            "workspace_board_section"
        ]
        workspace: models.Workspace = workspace_board_section.workspace

        # Then we filter the list of labels for labels that are contained
        # in this workspace
        label_uuids: list[UUID] = data.pop("labels")
        # Restrict to this workspace's labels, if there are too many
        # labels throw a ValidationError
        labels = list(workspace.label_set.filter(uuid__in=label_uuids))
        label_mapping = {label.uuid: label for label in labels}
        label_not_contained = any(
            label_uuid not in label_mapping for label_uuid in label_uuids
        )
        if label_not_contained:
            raise serializers.ValidationError(
                {
                    "labels": _(
                        "At least one specified label could not be found "
                        "in the task's workspace"
                    )
                }
            )

        # Then we check if the assignee is part of this workspace
        assignee_uuid: Optional[str] = data.pop("assignee")
        try:
            assignee = (
                assignee_uuid
                and workspace.workspaceuser_set.filter(
                    uuid=assignee_uuid
                ).get()
            )
        except models.WorkspaceUser.DoesNotExist:
            raise serializers.ValidationError(
                {
                    "assignee": _("The assignee could not be found"),
                }
            )

        return {
            **data,
            "workspace": workspace,
            "labels": labels,
            "assignee": assignee,
        }

    # This doesn't prevent deleting a label after validation, but it gets
    # us far enough. Further transaction handling should happen in the views
    # instead.
    @transaction.atomic
    def create(self, validated_data: dict[str, Any]) -> models.Task:
        """Create the task and assign label / ws user."""
        labels: list[models.Label] = validated_data.pop("labels")
        task = super().create(validated_data)
        assign_labels(task, labels)
        return task

    @transaction.atomic
    def update(
        self, instance: models.Task, validated_data: dict[str, Any]
    ) -> models.Task:
        """Assign labels, assign assignee."""
        labels: list[models.Label] = validated_data.pop("labels")
        task = super().update(instance, validated_data)
        assign_labels(task, labels)
        return task

    class Meta(base.TaskBaseSerializer.Meta):
        """Meta."""

        fields = (
            *base.TaskBaseSerializer.Meta.fields,
            "workspace_board_section",
        )
