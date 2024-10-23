# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023 JWP Consulting GK
"""Task serializers."""

from rest_framework import serializers

from projectify.user.serializers import UserSerializer
from projectify.workspace.models.team_member import TeamMember

from . import (
    base,
)


class AssigneeSerializer(serializers.ModelSerializer[TeamMember]):
    """Serialize a task assignee."""

    user = UserSerializer(read_only=True)

    class Meta:
        """Meta."""

        model = TeamMember
        fields = (
            "user",
            "uuid",
            "role",
        )
        extra_kwargs = {
            "role": {"required": True},
        }


class TaskWithSubTaskSerializer(base.TaskBaseSerializer):
    """Serialize all task details."""

    labels = base.LabelBaseSerializer(many=True, read_only=True)
    assignee = AssigneeSerializer(read_only=True, allow_null=True)
    sub_tasks = base.SubTaskBaseSerializer(
        many=True, read_only=True, source="subtask_set"
    )

    class Meta(base.TaskBaseSerializer.Meta):
        """Meta."""

        fields = (
            *base.TaskBaseSerializer.Meta.fields,
            "sub_tasks",
            "labels",
            "assignee",
        )
