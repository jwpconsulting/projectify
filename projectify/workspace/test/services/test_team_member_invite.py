# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023-2024 JWP Consulting GK
"""Test TeamMemberInvite services."""

import pytest
from faker import Faker
from rest_framework import serializers

from projectify.user.models import User
from projectify.user.models.user_invite import UserInvite
from projectify.user.services.internal import user_create
from projectify.workspace.models.team_member import TeamMember
from projectify.workspace.models.team_member_invite import TeamMemberInvite
from projectify.workspace.models.workspace import Workspace
from projectify.workspace.services.team_member import team_member_delete
from projectify.workspace.services.team_member_invite import (
    team_member_invite_create,
    team_member_invite_delete,
)


@pytest.mark.django_db
class TestAddOrInviteTeamMember:
    """Test add_or_invite_team_member."""

    # We could probably use a more specific type for mailoutbox
    def test_invite_user(
        self,
        workspace: Workspace,
        mailoutbox: list[object],
        team_member: TeamMember,
    ) -> None:
        """Test inviting a user."""
        team_member_invite = team_member_invite_create(
            who=team_member.user,
            workspace=workspace,
            email_or_user="hello@example.com",
        )
        assert team_member_invite.workspace == workspace
        assert len(mailoutbox) == 1

    def test_invite_then_up(
        self,
        workspace: Workspace,
        team_member: TeamMember,
    ) -> None:
        """Test inviting with a sign up."""
        count = workspace.users.count()
        team_member_invite_create(
            who=team_member.user,
            workspace=workspace,
            email_or_user="hello@example.com",
        )
        assert workspace.users.count() == count
        user_create(email="hello@example.com")
        assert workspace.users.count() == count + 1

    def test_signs_up_twice(
        self,
        workspace: Workspace,
        team_member: TeamMember,
    ) -> None:
        """Test what happens if a user signs up twice."""
        count = workspace.users.count()
        team_member_invite_create(
            who=team_member.user,
            workspace=workspace,
            email_or_user="hello@example.com",
        )
        user = user_create(email="hello@example.com")
        assert workspace.users.count() == count + 1
        user.delete()
        assert workspace.users.count() == count
        user = user_create(email="hello@example.com")
        # The user is not automatically added
        assert workspace.users.count() == count

    def test_inviting_twice(
        self, workspace: Workspace, team_member: TeamMember
    ) -> None:
        """Test that inviting twice won't work."""
        team_member_invite_create(
            who=team_member.user,
            workspace=workspace,
            email_or_user="hello@example.com",
        )
        with pytest.raises(serializers.ValidationError):
            team_member_invite_create(
                who=team_member.user,
                workspace=workspace,
                email_or_user="hello@example.com",
            )

    def test_inviting_team_member(
        self, workspace: Workspace, team_member: TeamMember
    ) -> None:
        """Test that inviting a pre-existing user won't work."""
        with pytest.raises(serializers.ValidationError):
            team_member_invite_create(
                workspace=workspace,
                who=team_member.user,
                email_or_user=team_member.user.email,
            )

    def test_inviting_user(
        self,
        workspace: Workspace,
        unrelated_user: User,
        team_member: TeamMember,
    ) -> None:
        """Test that inviting an existing user will work."""
        count = workspace.teammember_set.count()
        team_member_invite_create(
            workspace=workspace,
            who=team_member.user,
            email_or_user=unrelated_user.email,
        )
        assert workspace.teammember_set.count() == count + 1

    def test_uninviting_user(
        self, team_member: TeamMember, workspace: Workspace
    ) -> None:
        """Test uninviting a user."""
        count = workspace.teammemberinvite_set.count()
        team_member_invite_create(
            who=team_member.user,
            workspace=workspace,
            email_or_user="hello@example.com",
        )
        assert workspace.teammemberinvite_set.count() == count + 1
        team_member_invite_delete(
            workspace=workspace,
            who=team_member.user,
            email="hello@example.com",
        )
        assert workspace.teammemberinvite_set.count() == count

    def test_after_uninvite(
        self,
        workspace: Workspace,
        team_member: TeamMember,
    ) -> None:
        """Test what happens when a user is uninvited."""
        count = workspace.users.count()
        team_member_invite_create(
            who=team_member.user,
            workspace=workspace,
            email_or_user="hello@example.com",
        )
        assert workspace.users.count() == count
        team_member_invite_delete(
            who=team_member.user,
            workspace=workspace,
            email="hello@example.com",
        )
        user_create(email="hello@example.com")
        # The user is not added
        assert workspace.users.count() == count

    def test_uninviting_user_on_no_invite(
        self, team_member: TeamMember, workspace: Workspace
    ) -> None:
        """Test uninviting a user that was never invited."""
        count = workspace.teammemberinvite_set.count()
        with pytest.raises(serializers.ValidationError) as error:
            team_member_invite_delete(
                workspace=workspace,
                who=team_member.user,
                email="hello@example.com",
            )
        assert error.match("was never invited")
        assert workspace.teammemberinvite_set.count() == count

    def test_invite_redeem_delete_invite_redeem(
        self,
        workspace: Workspace,
        team_member: TeamMember,
        faker: Faker,
    ) -> None:
        """Test entire life cycle and make sure redeemed invites are not redeemed twice."""
        email = faker.email()
        count = workspace.users.count()

        # Blank slate
        assert TeamMemberInvite.objects.count() == 0
        assert UserInvite.objects.count() == 0

        # Invite new user
        invite = team_member_invite_create(
            who=team_member.user, workspace=workspace, email_or_user=email
        )
        assert isinstance(invite, TeamMemberInvite)

        # There is one team member invite
        assert TeamMemberInvite.objects.count() == 1
        # And one user invite
        assert UserInvite.objects.count() == 1

        # New user accepts invitation
        user = user_create(email=email)
        assert workspace.users.count() == count + 1

        # Invite is redeemed
        invite.refresh_from_db()
        assert invite.redeemed is True
        assert invite.redeemed_when is not None
        # Counts are unchanged
        assert TeamMemberInvite.objects.count() == 1
        assert UserInvite.objects.count() == 1

        # User deletes account
        user.delete()
        assert workspace.users.count() == count
        # Invites are deleted
        assert TeamMemberInvite.objects.count() == 0
        assert UserInvite.objects.count() == 0

        # User is invited again
        new_invite = team_member_invite_create(
            who=team_member.user, workspace=workspace, email_or_user=email
        )
        assert isinstance(new_invite, TeamMemberInvite)

        # User accepts invitation
        user = user_create(email=email)
        assert workspace.users.count() == count + 1
        new_team_member = TeamMember.objects.get(user=user)

        # Invite is redeemed
        new_invite.refresh_from_db()
        assert new_invite.redeemed is True
        assert new_invite.redeemed_when is not None
        # There is still only one invite
        assert TeamMemberInvite.objects.count() == 1
        assert UserInvite.objects.count() == 1

        # Team member is deleted
        team_member_delete(team_member=new_team_member, who=team_member.user)

        # TODO consider if an invite should be deleted as a consequence of ws
        # user deletion
        # Team member invite is still there
        assert TeamMemberInvite.objects.count() == 1
        # Invite is still there
        assert UserInvite.objects.count() == 1

        # User is invited one more time
        one_more_invite = team_member_invite_create(
            who=team_member.user, workspace=workspace, email_or_user=email
        )
        assert isinstance(one_more_invite, TeamMember)

        # Now, no new invites are created, so the count shall stay the same
        assert TeamMemberInvite.objects.count() == 1
        assert UserInvite.objects.count() == 1
