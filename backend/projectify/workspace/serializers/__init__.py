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
"""Workspace app serializers."""
from .base import (
    WorkspaceBaseSerializer,
    WorkspaceBoardBaseSerializer,
)
from .task_detail import (
    TaskCreateUpdateSerializer,
    TaskDetailSerializer,
)
from .workspace import (
    WorkspaceDetailSerializer,
)
from .workspace_board import (
    WorkspaceBoardDetailSerializer,
)
from .workspace_board_section import (
    WorkspaceBoardSectionDetailSerializer,
)

# XXX
# I don't like that we user the Base serializer here
__all__ = [
    "TaskDetailSerializer",
    "TaskCreateUpdateSerializer",
    "WorkspaceBaseSerializer",
    "WorkspaceBoardBaseSerializer",
    "WorkspaceBoardDetailSerializer",
    "WorkspaceBoardSectionDetailSerializer",
    "WorkspaceDetailSerializer",
]
