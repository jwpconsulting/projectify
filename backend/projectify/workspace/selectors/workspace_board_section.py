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
"""Workspace board section selectors."""
from typing import Optional
from uuid import UUID

from projectify.user.models import User
from projectify.workspace.models.workspace_board_section import (
    WorkspaceBoardSection,
)


def workspace_board_section_find_for_user_and_uuid(
    *,
    workspace_board_section_uuid: UUID,
    user: User,
) -> Optional[WorkspaceBoardSection]:
    """Find a workspace board section given a UUID and a user."""
    try:
        return WorkspaceBoardSection.objects.filter_for_user_and_uuid(
            user=user,
            uuid=workspace_board_section_uuid,
        ).get()
    except WorkspaceBoardSection.DoesNotExist:
        return None
