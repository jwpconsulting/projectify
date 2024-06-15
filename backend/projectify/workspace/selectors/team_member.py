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
"""Team member selectors."""
from typing import Optional
from uuid import UUID

from projectify.user.models import User
from projectify.workspace.models.team_member import TeamMember
from projectify.workspace.models.workspace import Workspace


def team_member_find_for_workspace(
    *, user: User, workspace: Workspace
) -> Optional[TeamMember]:
    """Find a team member."""
    try:
        return TeamMember.objects.get(workspace=workspace, user=user)
    except TeamMember.DoesNotExist:
        return None


def team_member_find_by_team_member_uuid(
    *, who: User, team_member_uuid: UUID
) -> Optional[TeamMember]:
    """Find team member by UUID according to user access permissions."""
    try:
        return TeamMember.objects.select_related("user").get(
            workspace__users=who, uuid=team_member_uuid
        )
    except TeamMember.DoesNotExist:
        return None
