# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023 JWP Consulting GK
"""Team member services."""

from typing import Optional

from django.db import transaction
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from projectify.lib.auth import validate_perm
from projectify.user.models import User
from projectify.workspace.models.const import TeamMemberRoles
from projectify.workspace.models.team_member import TeamMember
from projectify.workspace.services.signals import send_change_signal


@transaction.atomic
def team_member_update(
    *,
    team_member: TeamMember,
    who: User,
    job_title: Optional[str] = None,
    role: TeamMemberRoles,
) -> TeamMember:
    """Update a team member with new role and job title."""
    validate_perm("workspace.update_team_member", who, team_member.workspace)
    team_member.job_title = job_title
    team_member.role = role
    team_member.save()
    send_change_signal("changed", team_member.workspace)
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
    validate_perm("workspace.delete_team_member", who, team_member.workspace)
    if team_member.user == who:
        raise serializers.ValidationError(
            {"team_member": _("Can't delete own team member")}
        )
    team_member.delete()
    send_change_signal("changed", team_member.workspace)
