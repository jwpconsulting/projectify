# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023 JWP Consulting GK
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
