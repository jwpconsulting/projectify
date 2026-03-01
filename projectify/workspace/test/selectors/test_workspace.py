# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2024 JWP Consulting GK
"""Test workspace model selectors."""

import pytest

from ...models import TeamMember, TeamMemberInvite
from ...selectors.workspace import (
    WorkspaceDetailQuerySet,
    workspace_find_by_workspace_uuid,
    workspace_find_for_user,
)
from ...services.workspace import workspace_delete

pytestmark = pytest.mark.django_db


def test_workspace_find_for_user(
    team_member: TeamMember, unrelated_team_member: TeamMember
) -> None:
    """Test workspace_find_for_user."""
    a = team_member
    b = unrelated_team_member
    assert workspace_find_for_user(who=a.user).count() == 1
    assert workspace_find_for_user(who=b.user).count() == 1
    workspace_delete(who=a.user, workspace=a.workspace)
    assert workspace_find_for_user(who=a.user).count() == 0
    assert workspace_find_for_user(who=b.user).count() == 1
    workspace_delete(who=b.user, workspace=b.workspace)
    assert workspace_find_for_user(who=a.user).count() == 0
    assert workspace_find_for_user(who=b.user).count() == 0


def test_workspace_find_by_workspace_uuid(
    team_member: TeamMember, unrelated_team_member: TeamMember
) -> None:
    """Test workspace_find_by_workspace_uuid."""
    a = team_member
    b = unrelated_team_member
    # A can find A's workspace
    assert workspace_find_by_workspace_uuid(
        who=a.user, workspace_uuid=a.workspace.uuid
    )
    # B can find B's workspace
    assert workspace_find_by_workspace_uuid(
        who=b.user, workspace_uuid=b.workspace.uuid
    )
    # A can't find B's workspace
    assert (
        workspace_find_by_workspace_uuid(
            who=a.user, workspace_uuid=b.workspace.uuid
        )
        is None
    )
    # B can't find A's workspace
    assert (
        workspace_find_by_workspace_uuid(
            who=b.user, workspace_uuid=a.workspace.uuid
        )
        is None
    )


def test_queryset_prefetch_refresh(
    team_member: TeamMember,
    team_member_invite: TeamMemberInvite,
) -> None:
    """Test that redeemed invites don't show up."""
    who = team_member.user
    wuid = team_member.workspace.uuid
    qs = WorkspaceDetailQuerySet
    ws = workspace_find_by_workspace_uuid(who=who, workspace_uuid=wuid, qs=qs)
    assert ws is not None
    invites = ws.active_invites
    assert invites
    assert len(invites) == 1

    team_member_invite.redeemed = True
    team_member_invite.save()

    ws = workspace_find_by_workspace_uuid(who=who, workspace_uuid=wuid, qs=qs)
    assert ws is not None
    invites = ws.active_invites
    assert invites is not None
    assert len(invites) == 0

    ws.refresh_from_db()
    invites = ws.active_invites
    assert invites is not None
    assert len(invites) == 0


def test_prefetch_deleted_invite(
    team_member: TeamMember,
    team_member_invite: TeamMemberInvite,
) -> None:
    """Test that redeemed invites don't show up."""
    who = team_member.user
    wuid = team_member.workspace.uuid
    qs = WorkspaceDetailQuerySet
    ws = workspace_find_by_workspace_uuid(who=who, workspace_uuid=wuid, qs=qs)
    assert ws is not None
    invites = ws.active_invites
    assert invites
    assert len(invites) == 1

    team_member_invite.delete()
    assert TeamMemberInvite.objects.count() == 0

    ws.refresh_from_db(from_queryset=qs)
    invites = ws.active_invites
    assert invites is not None
    assert len(invites) == 0
