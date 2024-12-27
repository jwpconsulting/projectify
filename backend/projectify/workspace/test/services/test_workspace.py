# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023-2024 JWP Consulting GK
"""Test workspace services."""

import pytest
from faker import Faker
from rest_framework.exceptions import ValidationError

from projectify.user.models.user import User
from projectify.workspace.models.project import Project
from projectify.workspace.models.team_member import TeamMember
from projectify.workspace.models.workspace import Workspace
from projectify.workspace.services.project import project_delete
from projectify.workspace.services.team_member import team_member_delete
from projectify.workspace.services.team_member_invite import (
    team_member_invite_create,
    team_member_invite_delete,
)
from projectify.workspace.services.workspace import workspace_delete

pytestmark = pytest.mark.django_db


def test_workspace_delete(
    workspace: Workspace,
    user: User,
) -> None:
    """Test that a freshly created workspace from a fixture can be deleted."""
    count = Workspace.objects.count()
    workspace_delete(workspace=workspace, who=user)
    assert Workspace.objects.count() == count - 1


def test_workspace_delete_dependencies(
    workspace: Workspace,
    project: Project,
    other_team_member: TeamMember,
    user: User,
    faker: Faker,
) -> None:
    """Test that a freshly created workspace from a fixture can be deleted."""
    count = Workspace.objects.count()

    invite_email = faker.email()
    team_member_invite_create(
        who=user,
        workspace=workspace,
        email_or_user=invite_email,
    )

    with pytest.raises(ValidationError) as error:
        workspace_delete(workspace=workspace, who=user)
    assert error.match("one remaining team member")
    team_member_delete(team_member=other_team_member, who=user)

    with pytest.raises(ValidationError) as error:
        workspace_delete(workspace=workspace, who=user)
    assert error.match("no outstanding invites")

    team_member_invite_delete(
        who=user, email=invite_email, workspace=workspace
    )

    with pytest.raises(ValidationError) as error:
        workspace_delete(workspace=workspace, who=user)
    assert error.match("no projects")

    # Finally it will work
    project_delete(who=user, project=project)
    workspace_delete(workspace=workspace, who=user)
    assert Workspace.objects.count() == count - 1
