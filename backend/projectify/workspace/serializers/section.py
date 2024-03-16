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
from projectify.workspace.serializers.task import (
    TaskWithSubTaskSerializer,
)

from . import (
    base,
)


class ProjectUpSerializer(base.ProjectBaseSerializer):
    """
    Serialize project and workspace containing it.

    Used when serializing up from a task or ws board section.
    """

    workspace = base.WorkspaceBaseSerializer(read_only=True)

    class Meta(base.ProjectBaseSerializer.Meta):
        """Meta."""

        fields = (
            *base.ProjectBaseSerializer.Meta.fields,
            "workspace",
        )


class SectionUpSerializer(base.SectionBaseSerializer):
    """Serialize section up the hierarchy."""

    project = ProjectUpSerializer(read_only=True)

    class Meta(base.SectionBaseSerializer.Meta):
        """Meta."""

        fields = (
            *base.SectionBaseSerializer.Meta.fields,
            "project",
        )


class SectionDetailSerializer(base.SectionBaseSerializer):
    """
    Section detail serializer.

    Goes both up (to workspace) and down (all tasks).
    """

    project = ProjectUpSerializer(read_only=True)
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
