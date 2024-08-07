# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Copyright (C) 2023 JWP Consulting GK
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
