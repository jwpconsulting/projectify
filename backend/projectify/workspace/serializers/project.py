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
"""Project serializers."""
from rest_framework import serializers

from projectify.workspace.models.project import Project
from projectify.workspace.models.section import Section
from projectify.workspace.models.task import Task
from projectify.workspace.serializers.base import (
    LabelBaseSerializer,
    ProjectBaseSerializer,
    TeamMemberBaseSerializer,
)
from projectify.workspace.serializers.workspace import (
    WorkspaceDetailSerializer,
)


class ProjectDetailTaskSerializer(serializers.ModelSerializer[Task]):
    """Serialize all task details."""

    labels = LabelBaseSerializer(many=True, read_only=True)
    assignee = TeamMemberBaseSerializer(read_only=True, allow_null=True)
    # TODO Justus 2024-04-09
    # This can be simplified as well, might only have to return completion
    # percentage
    sub_task_progress = serializers.FloatField(allow_null=True)

    class Meta:
        """Meta."""

        # Leaving out created, updated
        model = Task
        fields = (
            "title",
            "uuid",
            "due_date",
            "number",
            "labels",
            "assignee",
            "sub_task_progress",
            # TODO
            # We want to optimize description away in the future but for now,
            # since we require a complete retransmission of a task in order for
            # it to be updated, we need to hold a complete copy of it. Only
            # this way we can perform updates from the FE dashboard.
            "description",
        )
        extra_kwargs = {
            "description": {"required": True},
            "due_date": {"required": True},
        }


class ProjectDetailSectionSerializer(serializers.ModelSerializer[Section]):
    """Reduced section serializer."""

    tasks = ProjectDetailTaskSerializer(
        many=True, read_only=True, source="task_set"
    )

    class Meta:
        """Meta."""

        model = Section
        fields = (
            "uuid",
            "_order",
            "title",
            "tasks",
            "description",
        )
        extra_kwargs = {
            "description": {"required": True},
        }


class ProjectDetailSerializer(ProjectBaseSerializer):
    """
    Project serializer.

    Serializes in both directions, workspace and sections, including their
    tasks.
    """

    sections = ProjectDetailSectionSerializer(
        many=True, read_only=True, source="section_set"
    )

    workspace = WorkspaceDetailSerializer(read_only=True)

    class Meta(ProjectBaseSerializer.Meta):
        """Meta."""

        model = Project
        fields = (
            *ProjectBaseSerializer.Meta.fields,
            "sections",
            "workspace",
        )
