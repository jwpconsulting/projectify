# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023-2024 JWP Consulting GK
"""Test workspace services."""

from typing import cast

from django import db
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.models.fields.files import FileDescriptor

import pytest
from faker import Faker
from rest_framework.exceptions import ValidationError

from projectify.user.models.user import User
from projectify.workspace.models.const import TeamMemberRoles
from projectify.workspace.models.project import Project
from projectify.workspace.models.team_member import TeamMember
from projectify.workspace.models.workspace import Workspace
from projectify.workspace.services.project import project_delete
from projectify.workspace.services.team_member import team_member_delete
from projectify.workspace.services.team_member_invite import (
    team_member_invite_create,
    team_member_invite_delete,
)
from projectify.workspace.services.workspace import (
    workspace_add_user,
    workspace_delete,
    workspace_update,
)

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


def test_workspace_update(
    workspace: Workspace,
    user: User,
    faker: Faker,
    uploaded_file: SimpleUploadedFile,
) -> None:
    """Test updating a workspace."""
    new_title = faker.company()
    new_description = faker.text()

    updated_workspace = workspace_update(
        workspace=workspace,
        title=new_title,
        description=new_description,
        picture=cast(FileDescriptor, uploaded_file),
        who=user,
    )

    updated_workspace.refresh_from_db()
    assert updated_workspace.title == new_title
    assert updated_workspace.description == new_description
    assert "picture/test" in updated_workspace.picture.path


def test_add_user(
    workspace: Workspace,
    other_user: User,
) -> None:
    """Test that adding a user twice won't work."""
    count = workspace.users.count()
    workspace_add_user(
        workspace=workspace, user=other_user, role=TeamMemberRoles.OBSERVER
    )
    assert workspace.users.count() == count + 1
    # XXX TODO should be validationerror, not integrityerror
    # We might get a bad 500 here, could be 400 instead
    with pytest.raises(db.IntegrityError):
        workspace_add_user(
            workspace=workspace, user=other_user, role=TeamMemberRoles.OBSERVER
        )
