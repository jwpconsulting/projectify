# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023-2024 JWP Consulting GK
"""Project serializers."""

from rest_framework import serializers

from projectify.user.serializers import UserSerializer

from ..models.project import Project
from ..models.section import Section
from ..models.task import Task
from ..models.team_member import TeamMember
from ..serializers.base import (
    LabelBaseSerializer,
    ProjectBaseSerializer,
)
from ..serializers.workspace import WorkspaceDetailSerializer


class ProjectTaskAssigneeSerializer(serializers.ModelSerializer[TeamMember]):
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


class ProjectDetailTaskSerializer(serializers.ModelSerializer[Task]):
    """Serialize all task details."""

    labels = LabelBaseSerializer(many=True, read_only=True)
    assignee = ProjectTaskAssigneeSerializer(read_only=True, allow_null=True)
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
            "description",
            "tasks",
        )


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
            "title",
            "description",
            "uuid",
            "archived",
            "sections",
            "workspace",
        )
