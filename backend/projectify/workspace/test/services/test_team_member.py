# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023 JWP Consulting GK
"""Test team member services."""

import pytest
from rest_framework.exceptions import PermissionDenied

from projectify.user.models import User
from projectify.workspace.models.const import TeamMemberRoles
from projectify.workspace.models.project import Project
from projectify.workspace.models.team_member import TeamMember
from projectify.workspace.models.workspace import Workspace
from projectify.workspace.services.team_member import (
    team_member_change_role,
    team_member_delete,
    team_member_update,
    team_member_visit_project,
    team_member_visit_workspace,
)
from projectify.workspace.services.workspace import workspace_add_user

pytestmark = pytest.mark.django_db


def test_team_member_update(team_member: TeamMember) -> None:
    """Test updating a team member."""
    # First, we update ourselves
    team_member_update(
        who=team_member.user,
        team_member=team_member,
        job_title="bla",
    )


def test_team_member_change_role(
    team_member: TeamMember, unrelated_user: User
) -> None:
    """Test changing team member roles."""
    with pytest.raises(PermissionDenied):
        team_member_change_role(
            who=team_member.user,
            team_member=team_member,
            role=TeamMemberRoles.OBSERVER,
        )
    new_team_member = workspace_add_user(
        workspace=team_member.workspace,
        # TODO perm check missing in workspace_add_user
        # E who=team_member.user,
        user=unrelated_user,
        role=TeamMemberRoles.OBSERVER,
    )
    team_member_change_role(
        who=team_member.user,
        team_member=new_team_member,
        role=TeamMemberRoles.OWNER,
    )


def test_team_member_delete(
    team_member: TeamMember,
    unrelated_user: User,
) -> None:
    """Test deleting a team member after adding them."""
    count = team_member.workspace.users.count()
    new_team_member = workspace_add_user(
        workspace=team_member.workspace,
        # TODO perm check missing in workspace_add_user
        # E who=team_member.user,
        user=unrelated_user,
        role=TeamMemberRoles.OBSERVER,
    )
    assert team_member.workspace.users.count() == count + 1
    team_member_delete(team_member=new_team_member, who=team_member.user)
    assert team_member.workspace.users.count() == count


def test_team_member_visit_workspace_permission_denied(
    unrelated_workspace: Workspace, user: User
) -> None:
    """Test that user without workspace access cannot visit workspace."""
    with pytest.raises(PermissionDenied):
        team_member_visit_workspace(user=user, workspace=unrelated_workspace)


def test_team_member_visit_project_permission_denied(
    unrelated_project: Project, user: User
) -> None:
    """Test that user without workspace access cannot visit project."""
    with pytest.raises(PermissionDenied):
        team_member_visit_project(user=user, project=unrelated_project)
