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
