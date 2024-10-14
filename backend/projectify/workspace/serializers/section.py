# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023 JWP Consulting GK
"""Section serializers."""

from rest_framework import serializers

from projectify.workspace.models.workspace import Workspace

from ..models.project import Project
from ..serializers.task import TaskWithSubTaskSerializer
from . import base


class SectionDetailWorkspaceSerializer(serializers.ModelSerializer[Workspace]):
    """Serialize a section's workspace."""

    class Meta:
        """Meta."""

        model = Workspace
        fields = (
            "title",
            "uuid",
        )


class SectionDetailProjectSerializer(serializers.ModelSerializer[Project]):
    """Serialize a project's section."""

    workspace = SectionDetailWorkspaceSerializer(read_only=True)

    class Meta:
        """Meta."""

        model = Project
        fields = (
            "title",
            "uuid",
            "workspace",
        )


class SectionUpSerializer(base.SectionBaseSerializer):
    """Serialize section up the hierarchy."""

    project = SectionDetailProjectSerializer(read_only=True)

    class Meta(base.SectionBaseSerializer.Meta):
        """Meta."""

        fields = (
            *base.SectionBaseSerializer.Meta.fields,
            "project",
        )
        extra_kwargs = {
            "description": {"required": True},
        }


class SectionDetailSerializer(base.SectionBaseSerializer):
    """
    Section detail serializer.

    Goes both up (to workspace) and down (all tasks).
    """

    project = SectionDetailProjectSerializer(read_only=True)
    tasks = TaskWithSubTaskSerializer(
        many=True, read_only=True, source="task_set"
    )

    class Meta(base.SectionBaseSerializer.Meta):
        """Meta."""

        fields = (
            *base.SectionBaseSerializer.Meta.fields,
            "project",
            "tasks",
        )
