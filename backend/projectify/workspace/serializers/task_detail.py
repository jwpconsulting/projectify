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
from collections import Counter
from collections.abc import Sequence
from typing import Any, Optional, TypedDict
from uuid import UUID

from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from rest_framework.request import Request

from projectify.user.models.user import User
from projectify.workspace.models.project import Project
from projectify.workspace.models.sub_task import SubTask

from ..models.section import Section
from ..models.task import Task
from ..models.team_member import TeamMember
from ..models.workspace import Workspace
from ..selectors.section import section_find_for_user_and_uuid
from ..serializers.base import (
    ChatMessageBaseSerializer,
    TaskBaseSerializer,
    UuidObjectSerializer,
)
from ..services.sub_task import (
    ValidatedData,
    ValidatedDatum,
    ValidatedDatumWithUuid,
)
from .task import TaskWithSubTaskSerializer


class TaskDetailWorkspaceSerializer(serializers.ModelSerializer[Workspace]):
    """Serializes a task's workspace."""

    class Meta:
        """Meta."""

        model = Workspace
        fields = (
            "title",
            "uuid",
        )
        extra_kwargs = {
            "description": {"required": True},
        }


class TaskDetailProjectSerializer(serializers.ModelSerializer[Project]):
    """Serialize a task's project."""

    workspace = TaskDetailWorkspaceSerializer(read_only=True)

    class Meta:
        """Meta."""

        model = Project
        fields = (
            "title",
            "uuid",
            "workspace",
            # TODO not needed?
            "description",
            "due_date",
        )
        extra_kwargs = {
            "due_date": {"required": True},
            "description": {"required": True},
        }


class TaskDetailSectionSerializer(serializers.ModelSerializer[Section]):
    """Serialize a task's section."""

    project = TaskDetailProjectSerializer(read_only=True)

    class Meta:
        """Meta."""

        model = Section
        fields = (
            "title",
            "uuid",
            "project",
            # TODO consider removing:
            "description",
            "_order",
        )
        extra_kwargs = {
            "description": {"required": True},
        }


class TaskDetailSerializer(TaskWithSubTaskSerializer):
    """
    Serialize all task details.

    Serializes up to the workspace in one direction, and all chat messages,
    labels and sub task in the other direction.
    """

    chat_messages = ChatMessageBaseSerializer(
        many=True, read_only=True, source="chatmessage_set"
    )
    section = TaskDetailSectionSerializer(read_only=True)

    class Meta(TaskWithSubTaskSerializer.Meta):
        """Meta."""

        fields = (
            *TaskWithSubTaskSerializer.Meta.fields,
            "chat_messages",
            "section",
        )
        extra_kwargs = {
            "due_date": {"required": True},
            "description": {"required": True},
        }


class UuidDict(TypedDict):
    """A dict containing a uuid."""

    uuid: UUID


class SubTaskCreateUpdateSerializer(serializers.ModelSerializer[SubTask]):
    """A sub task serializer that accepts a missing UUID."""

    uuid = serializers.UUIDField(required=False)

    class Meta:
        """Use the modified ListSerializer."""

        model = SubTask
        fields = (
            "uuid",
            "title",
            "description",
            "done",
        )


class TaskCreateUpdateSerializer(TaskBaseSerializer):
    """
    Serialize create or update information for a task.

    Instead of serializing label and assignee, it accepts label uuids and
    assignee uuid and evaluates them.

    Don't use directly, use TaskCreateSerializer or TaskUpdateSerializer
    instead.
    """

    # TODO make label optional, when unset remove labels or on create
    # do not assign label
    labels = serializers.ListField(
        child=UuidObjectSerializer(),
        write_only=True,
        # TODO required=False,
    )
    # TODO make assignee optional
    # assignee = UuidObjectSerializer(required=False, write_only=True)
    # Then interpret missing as delete assignee
    assignee = UuidObjectSerializer(allow_null=True)

    sub_tasks = SubTaskCreateUpdateSerializer(many=True, required=False)

    def validate_sub_tasks(self, value: list[Any]) -> ValidatedData:
        """Ensure that this task has no sub tasks when creating."""
        if self.instance:
            instance_sub_tasks = list(self.instance.subtask_set.all())
        else:
            instance_sub_tasks = None
        # We might be creating new sub tasks.
        # 1) determine which sub tasks have to be newly created
        create_sub_tasks: list[ValidatedDatum] = [
            {
                "title": sub_task["title"],
                "description": sub_task.get("description"),
                "done": sub_task["done"],
                "_order": order,
            }
            for order, sub_task in enumerate(value)
            if "uuid" not in sub_task
        ]
        # 2) determine which sub tasks have to be updated
        update_sub_tasks: list[ValidatedDatumWithUuid] = [
            {
                "uuid": sub_task["uuid"],
                "title": sub_task["title"],
                "description": sub_task.get("description"),
                "done": sub_task["done"],
                "_order": order,
            }
            for order, sub_task in enumerate(value)
            if "uuid" in sub_task
        ]
        # 2a) If there are updatable sub tasks, we must have instance data
        if self.instance is None and len(update_sub_tasks):
            # XXX
            # This error is not correctly formatted
            raise serializers.ValidationError(
                [
                    {
                        "uuid": _(
                            "Sub tasks to be updated have been specified, but no sub "
                            "task instances were provided."
                        )
                    }
                    for _ in value
                ]
            )
        # 3) check that UUIDs are not duplicated
        update_uuids = [sub_task["uuid"] for sub_task in update_sub_tasks]
        update_uuids_unique = set(update_uuids)
        if len(update_uuids_unique) < len(update_uuids):
            c = Counter(update_uuids)
            raise serializers.ValidationError(
                [
                    {
                        "uuid": _(
                            "Duplicate UUID found among sub tasks to be updated"
                        )
                    }
                    if c[s] > 1
                    else {}
                    for s in update_uuids
                ]
            )
        # 4) check that all update UUIDs are part of instance sub tasks
        #
        # Otherwise, that would mean we are updating a sub task that we did not
        # pass in as an instance. We only need to check this if we are
        # updating. create_sub_tasks by definition can not contain UUIDs
        if instance_sub_tasks is not None:
            instance_uuids = set(
                sub_task.uuid for sub_task in instance_sub_tasks
            )
            missing_uuids = update_uuids_unique - instance_uuids
            if len(missing_uuids) > 0:
                errors = [
                    {
                        "uuid": _(
                            f"Sub task {v['uuid']} could not be "
                            "found amount the instance data. Check whether "
                            "you have correctly passed all task's sub task "
                            "instances."
                        )
                    }
                    if v.get("uuid") in missing_uuids
                    else {}
                    for v in value
                ]
                raise serializers.ValidationError(detail=errors)
        # But: The opposite, a UUID in our update sub task UUIDs not being
        # present does not mean it was forgotten. It means that the sub task
        # shall be deleted in update()
        #
        # 5) Check that when... what was I going to write here?
        return {
            "create_sub_tasks": create_sub_tasks,
            "update_sub_tasks": update_sub_tasks,
        }

    def _validate(
        self,
        data: dict[str, Any],
        workspace: Workspace,
    ) -> dict[str, Any]:
        """Validate user access to ws board sect, assignee and labels."""
        # Then we filter the list of labels for labels that are contained
        # in this workspace
        label_uuids: list[UUID] = [
            label["uuid"] for label in data.pop("labels")
        ]
        # Restrict to this workspace's labels, if there are too many
        # labels throw a ValidationError
        labels = workspace.label_set.filter(uuid__in=label_uuids)
        found_label_uuids = list(labels.values_list("uuid", flat=True))
        is_missing = [u not in found_label_uuids for u in label_uuids]
        if any(is_missing):
            errors = [
                {"uuid": _("This label could not be found")} if missing else {}
                for missing in is_missing
            ]
            raise serializers.ValidationError({"labels": errors})

        # Then we check if the assignee is part of this workspace
        assignee_uuid: Optional[UuidDict] = data.pop("assignee")
        if assignee_uuid:
            try:
                assignee = workspace.teammember_set.filter(
                    uuid=assignee_uuid["uuid"]
                ).get()
            except TeamMember.DoesNotExist:
                raise serializers.ValidationError(
                    {"assignee": _("The assignee could not be found")}
                )
        else:
            assignee = None

        return {
            **data,
            "workspace": workspace,
            "labels": list(labels),
            "assignee": assignee,
        }

    def create(self, validated_data: dict[str, Any]) -> Task:
        """Do not call this method."""
        del validated_data
        raise NotImplementedError("Don't call")

    def update(self, instance: Task, validated_data: dict[str, Any]) -> Task:
        """Do not call this method."""
        del instance
        del validated_data
        raise NotImplementedError("Don't call")

    def save(self, **kwargs: Any) -> Task:
        """Do not call this method."""
        del kwargs
        raise NotImplementedError("Don't call")

    class Meta(TaskBaseSerializer.Meta):
        """Meta."""

        fields: Sequence[str] = (
            "title",
            "description",
            "assignee",
            "labels",
            "due_date",
            "sub_tasks",
        )


class TaskCreateSerializer(TaskCreateUpdateSerializer):
    """Serializer for creating tasks."""

    section = UuidObjectSerializer()

    def validate_section(
        self,
        value: UuidDict,
    ) -> Section:
        """Validate the section."""
        request: Request = self.context["request"]
        user: User = request.user

        # First, we make sure we are assigning the task to a project
        # section that the request's user has access to.
        section = section_find_for_user_and_uuid(
            user=user,
            section_uuid=value["uuid"],
        )
        if section is None:
            raise serializers.ValidationError(
                _("Section does not exist"),
            )
        # We pass the correct value back here, and use it for the three
        # dependent values label, assignee and sub task.
        # The question is whether we can put each into a separate validate_*
        # method and make ws board section available to them instead using
        # the serializer context.
        return section

    def validate(self, data: dict[str, Any]) -> dict[str, Any]:
        """
        Validate section based on section field.

        If you refer to TaskUpdateSerializer, you will see that section here
        comes from the task instance directly, since the task has already
        been created.
        """
        section: Section = data["section"]
        return self._validate(data, section.project.workspace)

    class Meta(TaskCreateUpdateSerializer.Meta):
        """Add section field."""

        fields = (
            *TaskCreateUpdateSerializer.Meta.fields,
            "section",
        )


class TaskUpdateSerializer(TaskCreateUpdateSerializer):
    """Serializer for updating tasks."""

    instance: Task

    def validate(self, data: dict[str, Any]) -> dict[str, Any]:
        """Run validation logic based off of given instance."""
        # TODO select related
        section: Section = self.instance.section
        return self._validate(data, section.project.workspace)

    class Meta(TaskCreateUpdateSerializer.Meta):
        """Meta."""

        fields = TaskCreateUpdateSerializer.Meta.fields
