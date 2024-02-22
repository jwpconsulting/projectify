# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Copyright (C) 2023-2024 JWP Consulting GK
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
"""Test WorkspaceUserInvite services."""
import pytest
from faker import Faker
from rest_framework import serializers

from projectify.user.models import User
from projectify.user.models.user_invite import UserInvite
from projectify.user.services.internal import user_create
from projectify.workspace.models.workspace import Workspace
from projectify.workspace.models.workspace_user import WorkspaceUser
from projectify.workspace.models.workspace_user_invite import (
    WorkspaceUserInvite,
)
from projectify.workspace.services.workspace_user import workspace_user_delete
from projectify.workspace.services.workspace_user_invite import (
    workspace_user_invite_create,
    workspace_user_invite_delete,
)

from ...exceptions import (
    UserAlreadyAdded,
    UserAlreadyInvited,
)


@pytest.mark.django_db
class TestAddOrInviteWorkspaceUser:
    """Test add_or_invite_workspace_user."""

    # We could probably use a more specific type for mailoutbox
    def test_invite_user(
        self,
        workspace: Workspace,
        mailoutbox: list[object],
        workspace_user: WorkspaceUser,
    ) -> None:
        """Test inviting a user."""
        workspace_user_invite = workspace_user_invite_create(
            who=workspace_user.user,
            workspace=workspace,
            email_or_user="hello@example.com",
        )
        assert workspace_user_invite.workspace == workspace
        assert len(mailoutbox) == 1

    def test_invite_then_up(
        self,
        workspace: Workspace,
        workspace_user: WorkspaceUser,
    ) -> None:
        """Test inviting with a sign up."""
        count = workspace.users.count()
        workspace_user_invite_create(
            who=workspace_user.user,
            workspace=workspace,
            email_or_user="hello@example.com",
        )
        assert workspace.users.count() == count
        user_create(email="hello@example.com")
        assert workspace.users.count() == count + 1

    def test_signs_up_twice(
        self,
        workspace: Workspace,
        workspace_user: WorkspaceUser,
    ) -> None:
        """Test what happens if a user signs up twice."""
        count = workspace.users.count()
        workspace_user_invite_create(
            who=workspace_user.user,
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
        self, workspace: Workspace, workspace_user: WorkspaceUser
    ) -> None:
        """Test that inviting twice won't work."""
        workspace_user_invite_create(
            who=workspace_user.user,
            workspace=workspace,
            email_or_user="hello@example.com",
        )
        with pytest.raises(UserAlreadyInvited):
            workspace_user_invite_create(
                who=workspace_user.user,
                workspace=workspace,
                email_or_user="hello@example.com",
            )

    def test_inviting_workspace_user(
        self, workspace: Workspace, workspace_user: WorkspaceUser
    ) -> None:
        """Test that inviting a pre-existing user won't work."""
        with pytest.raises(UserAlreadyAdded):
            workspace_user_invite_create(
                workspace=workspace,
                who=workspace_user.user,
                email_or_user=workspace_user.user.email,
            )

    def test_inviting_user(
        self,
        workspace: Workspace,
        unrelated_user: User,
        workspace_user: WorkspaceUser,
    ) -> None:
        """Test that inviting an existing user will work."""
        count = workspace.workspaceuser_set.count()
        workspace_user_invite_create(
            workspace=workspace,
            who=workspace_user.user,
            email_or_user=unrelated_user.email,
        )
        assert workspace.workspaceuser_set.count() == count + 1

    def test_uninviting_user(
        self, workspace_user: WorkspaceUser, workspace: Workspace
    ) -> None:
        """Test uninviting a user."""
        count = workspace.workspaceuserinvite_set.count()
        workspace_user_invite_create(
            who=workspace_user.user,
            workspace=workspace,
            email_or_user="hello@example.com",
        )
        assert workspace.workspaceuserinvite_set.count() == count + 1
        workspace_user_invite_delete(
            workspace=workspace,
            who=workspace_user.user,
            email="hello@example.com",
        )
        assert workspace.workspaceuserinvite_set.count() == count

    def test_after_uninvite(
        self,
        workspace: Workspace,
        workspace_user: WorkspaceUser,
    ) -> None:
        """Test what happens when a user is uninvited."""
        count = workspace.users.count()
        workspace_user_invite_create(
            who=workspace_user.user,
            workspace=workspace,
            email_or_user="hello@example.com",
        )
        assert workspace.users.count() == count
        workspace_user_invite_delete(
            who=workspace_user.user,
            workspace=workspace,
            email="hello@example.com",
        )
        user_create(email="hello@example.com")
        # The user is not added
        assert workspace.users.count() == count

    def test_uninviting_user_on_no_invite(
        self, workspace_user: WorkspaceUser, workspace: Workspace
    ) -> None:
        """Test uninviting a user that was never invited."""
        count = workspace.workspaceuserinvite_set.count()
        with pytest.raises(serializers.ValidationError) as error:
            workspace_user_invite_delete(
                workspace=workspace,
                who=workspace_user.user,
                email="hello@example.com",
            )
        assert error.match("was never invited")
        assert workspace.workspaceuserinvite_set.count() == count

    def test_invite_redeem_delete_invite_redeem(
        self,
        workspace: Workspace,
        workspace_user: WorkspaceUser,
        faker: Faker,
    ) -> None:
        """Test entire life cycle and make sure redeemed invites are not redeemed twice."""
        email = faker.email()
        count = workspace.users.count()

        # Blank slate
        assert WorkspaceUserInvite.objects.count() == 0
        assert UserInvite.objects.count() == 0

        # Invite new user
        invite = workspace_user_invite_create(
            who=workspace_user.user, workspace=workspace, email_or_user=email
        )
        assert isinstance(invite, WorkspaceUserInvite)

        # There is one workspace user invite
        assert WorkspaceUserInvite.objects.count() == 1
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
        assert WorkspaceUserInvite.objects.count() == 1
        assert UserInvite.objects.count() == 1

        # User deletes account
        user.delete()
        assert workspace.users.count() == count
        # Invites are deleted
        assert WorkspaceUserInvite.objects.count() == 0
        assert UserInvite.objects.count() == 0

        # User is invited again
        new_invite = workspace_user_invite_create(
            who=workspace_user.user, workspace=workspace, email_or_user=email
        )
        assert isinstance(new_invite, WorkspaceUserInvite)

        # User accepts invitation
        user = user_create(email=email)
        assert workspace.users.count() == count + 1
        new_workspace_user = WorkspaceUser.objects.get(user=user)

        # Invite is redeemed
        new_invite.refresh_from_db()
        assert new_invite.redeemed is True
        assert new_invite.redeemed_when is not None
        # There is still only one invite
        assert WorkspaceUserInvite.objects.count() == 1
        assert UserInvite.objects.count() == 1

        # Workspace user is deleted
        workspace_user_delete(
            workspace_user=new_workspace_user, who=workspace_user.user
        )

        # TODO consider if an invite should be deleted as a consequence of ws
        # user deletion
        # Workspace user invite is still there
        assert WorkspaceUserInvite.objects.count() == 1
        # Invite is still there
        assert UserInvite.objects.count() == 1

        # User is invited one more time
        one_more_invite = workspace_user_invite_create(
            who=workspace_user.user, workspace=workspace, email_or_user=email
        )
        assert isinstance(one_more_invite, WorkspaceUser)

        # Now, no new invites are created, so the count shall stay the same
        assert WorkspaceUserInvite.objects.count() == 1
        assert UserInvite.objects.count() == 1
