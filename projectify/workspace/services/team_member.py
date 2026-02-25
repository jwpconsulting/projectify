# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023,2026 JWP Consulting GK
"""Team member services."""

from typing import Optional

from django.db import transaction
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from projectify.lib.auth import validate_perm
from projectify.user.models import User

from ..models.const import TeamMemberRoles
from ..models.project import Project
from ..models.team_member import TeamMember


@transaction.atomic
def team_member_update(
    *, team_member: TeamMember, who: User, job_title: Optional[str] = None
) -> TeamMember:
    """Update a team member."""
    validate_perm("workspace.update_team_member", who, team_member.workspace)
    team_member.job_title = job_title
    team_member.save()
    return team_member


@transaction.atomic
def team_member_change_role(
    *, team_member: TeamMember, who: User, role: TeamMemberRoles
) -> TeamMember:
    """Change a team member's role."""
    validate_perm("workspace.update_team_member_role", who, team_member)
    team_member.role = role
    team_member.save()
    return team_member


@transaction.atomic
def team_member_delete(*, team_member: TeamMember, who: User) -> None:
    """
    Delete a team member.

    Validate that own user can not be deleted.

    We do not support deleting one's own team member for now. This is
    to avoid that if a user is an admin, that they will leave the workspace
    inoperable.

    On the other hand, we might introduce a proper hand-off procedure,
    so big TODO maybe?
    """
    validate_perm("workspace.delete_team_member", who, team_member)
    if team_member.user == who:
        raise serializers.ValidationError(
            _("You can't remove yourself from this workspace")
        )
    team_member.delete()


def team_member_visit_workspace(*, team_member: TeamMember) -> None:
    """Mark a workspace as recently visited."""
    team_member.last_visited_workspace = now()
    team_member.save()


def team_member_visit_project(
    *, team_member: TeamMember, project: Project
) -> None:
    """Mark a workspace and project as recently visited."""
    assert team_member.workspace == project.workspace
    team_member.last_visited_project = project
    team_member.last_visited_workspace = now()
    team_member.save()


@transaction.atomic
def team_member_minimize_project_list(
    *, team_member: TeamMember, minimized: bool
) -> TeamMember:
    """Set the minimized state of the project list for a team member."""
    team_member.minimized_project_list = minimized
    team_member.save()
    return team_member


@transaction.atomic
def team_member_minimize_team_member_filter(
    *, team_member: TeamMember, minimized: bool
) -> TeamMember:
    """Set the minimized state of the team member filter for a team member."""
    team_member.minimized_team_member_filter = minimized
    team_member.save()
    return team_member


@transaction.atomic
def team_member_minimize_label_filter(
    *, team_member: TeamMember, minimized: bool
) -> TeamMember:
    """Set the minimized state of the label filter for a team member."""
    team_member.minimized_label_filter = minimized
    team_member.save()
    return team_member
