# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023-2024 JWP Consulting GK
"""
Workspace services.

This is where all workspace related services will live in the future.
"""

import logging
from typing import Optional

from django.db import transaction
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from projectify.corporate.services.customer import customer_create
from projectify.lib.auth import validate_perm
from projectify.user.models import User
from projectify.workspace.services.signals import send_change_signal

from ..models.const import TeamMemberRoles
from ..models.team_member import TeamMember
from ..models.workspace import Workspace

logger = logging.getLogger(__name__)


# Create
def workspace_create(
    *,
    title: str,
    description: Optional[str] = None,
    owner: User,
) -> Workspace:
    """Create a workspace."""
    # TODO validate that user can only create 1 unpaid workspace
    workspace = Workspace.objects.create(title=title, description=description)
    workspace_add_user(
        workspace=workspace, user=owner, role=TeamMemberRoles.OWNER
    )
    customer_create(
        who=owner,
        workspace=workspace,
        # TODO not sure if this is good or not. Every workspace starts as a
        # trial workspace with 2 seats.
        seats=2,
    )
    return workspace


# Update
def workspace_update(
    *,
    workspace: Workspace,
    title: str,
    description: Optional[str] = None,
    who: User,
) -> Workspace:
    """Update a workspace."""
    validate_perm(
        "workspace.update_workspace",
        who,
        workspace,
    )
    workspace.title = title
    workspace.description = description
    workspace.save()
    send_change_signal("changed", workspace)
    return workspace


# Delete
@transaction.atomic
def workspace_delete(
    *,
    who: User,
    workspace: Workspace,
) -> None:
    """
    Delete a workspace.

    The business rules for deleting workspaces haven't really been thought out
    so far, so it will only work under the following conditions:

    - 1 remaining team member
    - No open invites
    - No boards
    - No labels
    """
    validate_perm("workspace.delete_workspace", who, workspace)
    if workspace.teammember_set.count() > 1:
        raise serializers.ValidationError(
            _("Can only delete workspace with one remaining team member")
        )
    if workspace.teammemberinvite_set.exists():
        raise serializers.ValidationError(
            _("Can only delete workspace with no outstanding invites")
        )
    if workspace.project_set.exists():
        raise serializers.ValidationError(
            _("Can only delete workspace with no projects")
        )
    count, _info = workspace.teammember_set.all().delete()
    logger.info(
        "Deleting workspace %s, after having deleted %d users",
        workspace,
        count,
    )
    send_change_signal("gone", workspace)
    workspace.delete()


# TODO looks like this is a private method only to be used to create the
# initial user, or when adding users through invitations
def workspace_add_user(
    *,
    workspace: Workspace,
    user: User,
    role: TeamMemberRoles,
) -> TeamMember:
    """Add user to workspace. Return new team member."""
    team_member = workspace.teammember_set.create(user=user, role=role)
    send_change_signal("changed", workspace)
    return team_member
