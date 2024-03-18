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
"""Team member services."""
from typing import Optional

from django.db import transaction
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from projectify.lib.auth import validate_perm
from projectify.user.models import User
from projectify.workspace.models.const import TeamMemberRoles
from projectify.workspace.models.team_member import TeamMember
from projectify.workspace.services.signals import send_workspace_change_signal


@transaction.atomic
def team_member_update(
    *,
    team_member: TeamMember,
    who: User,
    job_title: Optional[str] = None,
    role: TeamMemberRoles,
) -> TeamMember:
    """Update a team member with new role and job title."""
    validate_perm(
        "workspace.update_team_member", who, team_member.workspace
    )
    team_member.job_title = job_title
    team_member.role = role
    team_member.save()
    send_workspace_change_signal(team_member.workspace)
    return team_member


@transaction.atomic
def team_member_delete(
    *,
    team_member: TeamMember,
    who: User,
) -> None:
    """
    Delete a team member.

    Validate that own user can not be deleted.

    We do not support deleting one's own team member for now. This is
    to avoid that if a user is an admin, that they will leave the workspace
    inoperable.

    On the other hand, we might introduce a proper hand-off procedure,
    so big TODO maybe?
    """
    validate_perm(
        "workspace.delete_team_member", who, team_member.workspace
    )
    if team_member.user == who:
        raise serializers.ValidationError(
            {"team_member": _("Can't delete own team member")}
        )
    team_member.delete()
    send_workspace_change_signal(team_member.workspace)
