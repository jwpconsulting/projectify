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
"""Project serializers."""
from projectify.workspace.serializers.task import (
    TaskWithSubTaskSerializer,
)

from . import (
    base,
)


class SectionSerializer(base.SectionBaseSerializer):
    """
    Section serializer.

    Serializers the tasks that it contains.
    """

    tasks = TaskWithSubTaskSerializer(
        many=True, read_only=True, source="task_set"
    )

    class Meta(base.SectionBaseSerializer.Meta):
        """Meta."""

        fields = (
            *base.SectionBaseSerializer.Meta.fields,
            "tasks",
        )


class ProjectDetailSerializer(base.ProjectBaseSerializer):
    """
    Project serializer.

    Serializes in both directions, workspace and sections, including their
    tasks.
    """

    sections = SectionSerializer(
        many=True, read_only=True, source="section_set"
    )

    workspace = base.WorkspaceBaseSerializer(read_only=True)

    class Meta(base.ProjectBaseSerializer.Meta):
        """Meta."""

        fields = (
            *base.ProjectBaseSerializer.Meta.fields,
            "sections",
            "workspace",
        )
