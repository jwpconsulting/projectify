# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Copyright (C) 2023-2024 JWP Consulting GK
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
Task detail serializer.

We have put this here to avoid circular reference problems,
because ws board section requires importing the task serializer.
"""
from typing import (
    Any,
    Optional,
    TypedDict,
)
from uuid import (
    UUID,
)

from django.utils.translation import gettext_lazy as _

from rest_framework import (
    serializers,
)
from rest_framework.request import (
    Request,
)

from projectify.user.models.user import User
from projectify.workspace.selectors.workspace_board_section import (
    workspace_board_section_find_for_user_and_uuid,
)

from .. import (
    models,
)
from . import (
    base,
)
from .sub_task import (
    SubTaskCreateUpdateSerializer,
)
from .task import (
    TaskWithSubTaskSerializer,
)
from .workspace_board_section import (
    WorkspaceBoardSectionUpSerializer,
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


class UuidDict(TypedDict):
    """A dict containing a uuid."""

    uuid: UUID


class TaskCreateUpdateSerializer(base.TaskBaseSerializer):
    """
    Serialize update information for a task.

    Instead of serializing label and assignee, it accepts label uuids and
    assignee uuid and evaluates them.
    """

    workspace_board_section = base.UuidObjectSerializer(write_only=True)
    # TODO make label optional, when unset remove labels or on create
    # do not assign label
    labels = serializers.ListField(
        child=base.UuidObjectSerializer(),
        write_only=True,
        # TODO required=False,
    )
    # TODO make assignee optional
    # assignee = base.UuidObjectSerializer(required=False, write_only=True)
    # Then interpret missing as delete assignee
    assignee = base.UuidObjectSerializer(allow_null=True, write_only=True)

    sub_tasks = SubTaskCreateUpdateSerializer(many=True, required=False)

    def validate_workspace_board_section(
        self,
        value: UuidDict,
    ) -> models.WorkspaceBoardSection:
        """Validate the workspace board section."""
        request: Request = self.context["request"]
        user: User = request.user

        # First, we make sure we are assigning the task to a workspace board
        # section that the request's user has access to.
        workspace_board_section = (
            workspace_board_section_find_for_user_and_uuid(
                user=user,
                workspace_board_section_uuid=value["uuid"],
            )
        )
        if workspace_board_section is None:
            raise serializers.ValidationError(
                _("Workspace board section does not exist"),
            )
        # TODO select related
        workspace = workspace_board_section.workspace_board.workspace
        if self.instance and self.instance.workspace != workspace:
            raise serializers.ValidationError(
                _("This task cannot be assigned to another workspace"),
            )
        # We pass the correct value back here, and use it for the three
        # dependent values label, assignee and sub task.
        # The question is whether we can put each into a separate validate_*
        # method and make ws board section available to them instead using
        # the serializer context.
        return workspace_board_section

    def validate(self, data: dict[str, Any]) -> dict[str, Any]:
        """Validate user access to ws board sect, assignee and labels."""
        workspace_board_section: models.WorkspaceBoardSection = data[
            "workspace_board_section"
        ]
        # TODO select related
        workspace = workspace_board_section.workspace_board.workspace

        # Then we filter the list of labels for labels that are contained
        # in this workspace
        label_uuids: list[UUID] = [
            label["uuid"] for label in data.pop("labels")
        ]
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
        assignee_uuid: Optional[UuidDict] = data.pop("assignee")
        try:
            assignee = (
                assignee_uuid
                and workspace.workspaceuser_set.filter(
                    uuid=assignee_uuid["uuid"]
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

    def create(self, validated_data: dict[str, Any]) -> models.Task:
        """Do not call this method."""
        raise NotImplementedError("Don't call")

    def update(
        self, instance: models.Task, validated_data: dict[str, Any]
    ) -> models.Task:
        """Do not call this method."""
        raise NotImplementedError("Don't call")

    def save(self, **kwargs: Any) -> models.Task:
        """Do not call this method."""
        raise NotImplementedError("Don't call")

    class Meta(base.TaskBaseSerializer.Meta):
        """Meta."""

        fields = (
            *base.TaskBaseSerializer.Meta.fields,
            "workspace_board_section",
            "sub_tasks",
        )
