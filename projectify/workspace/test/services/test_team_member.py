# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023,2026 JWP Consulting GK
"""Test team member services."""

import pytest
from rest_framework.exceptions import PermissionDenied

from projectify.user.models import User

from ...models import Project, TeamMember
from ...models.const import TeamMemberRoles
from ...services.team_member import (
    team_member_change_role,
    team_member_delete,
    team_member_minimize_label_filter,
    team_member_minimize_project_list,
    team_member_minimize_team_member_filter,
    team_member_update,
    team_member_visit_project,
    team_member_visit_workspace,
)
from ...services.workspace import workspace_add_user

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


def test_team_member_delete_self(team_member: TeamMember) -> None:
    """Test that you can't delete yourself, even superusers."""
    team_member.user.is_superuser = True
    team_member.user.save()
    with pytest.raises(PermissionDenied):
        team_member_delete(team_member=team_member, who=team_member.user)


def test_team_member_visit_functions(
    team_member: TeamMember, project: Project, other_project: Project
) -> None:
    """Test visiting a workspace and project."""
    team_member_visit_workspace(team_member=team_member)
    team_member_visit_project(team_member=team_member, project=project)
    with pytest.raises(AssertionError):
        team_member_visit_project(
            team_member=team_member, project=other_project
        )


def test_team_member_minimize_project_list(team_member: TeamMember) -> None:
    """Test setting the minimized state of the project list."""
    # False in the beginning
    assert team_member.minimized_project_list is False

    updated_team_member = team_member_minimize_project_list(
        team_member=team_member, minimized=True
    )
    assert updated_team_member.minimized_project_list is True

    updated_team_member = team_member_minimize_project_list(
        team_member=team_member, minimized=False
    )
    assert updated_team_member.minimized_project_list is False


def test_team_member_minimize_team_member_filter(
    team_member: TeamMember,
) -> None:
    """Test setting the minimized state of the team member filter."""
    assert team_member.minimized_team_member_filter is False

    updated_team_member = team_member_minimize_team_member_filter(
        team_member=team_member, minimized=True
    )
    assert updated_team_member.minimized_team_member_filter is True

    updated_team_member = team_member_minimize_team_member_filter(
        team_member=team_member, minimized=False
    )
    assert updated_team_member.minimized_team_member_filter is False


def test_team_member_minimize_label_filter(team_member: TeamMember) -> None:
    """Test setting the minimized state of the label filter."""
    assert team_member.minimized_label_filter is False

    updated_team_member = team_member_minimize_label_filter(
        team_member=team_member, minimized=True
    )
    assert updated_team_member.minimized_label_filter is True

    updated_team_member = team_member_minimize_label_filter(
        team_member=team_member, minimized=False
    )
    assert updated_team_member.minimized_label_filter is False
