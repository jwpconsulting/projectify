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
"""Workspace board section serializers."""
from projectify.workspace.serializers.task import (
    TaskWithSubTaskSerializer,
)

from . import (
    base,
)


class WorkspaceBoardUpSerializer(base.WorkspaceBoardBaseSerializer):
    """
    Serialize workspace board and workspace containing it.

    Used when serializing up from a task or ws board section.
    """

    workspace = base.WorkspaceBaseSerializer(read_only=True)

    class Meta(base.WorkspaceBoardBaseSerializer.Meta):
        """Meta."""

        fields = (
            *base.WorkspaceBoardBaseSerializer.Meta.fields,
            "workspace",
        )


class WorkspaceBoardSectionUpSerializer(
    base.WorkspaceBoardSectionBaseSerializer
):
    """Serialize workspace board section up the hierarchy."""

    workspace_board = WorkspaceBoardUpSerializer(read_only=True)

    class Meta(base.WorkspaceBoardSectionBaseSerializer.Meta):
        """Meta."""

        fields = (
            *base.WorkspaceBoardSectionBaseSerializer.Meta.fields,
            "workspace_board",
        )


class WorkspaceBoardSectionDetailSerializer(
    base.WorkspaceBoardSectionBaseSerializer
):
    """
    Workspace board section detail serializer.

    Goes both up (to workspace) and down (all tasks).
    """

    workspace_board = WorkspaceBoardUpSerializer(read_only=True)
    tasks = TaskWithSubTaskSerializer(
        many=True, read_only=True, source="task_set"
    )

    class Meta(base.WorkspaceBoardSectionBaseSerializer.Meta):
        """Meta."""

        fields = (
            *base.WorkspaceBoardSectionBaseSerializer.Meta.fields,
            "workspace_board",
            "tasks",
        )
