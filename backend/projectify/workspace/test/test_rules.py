# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Copyright (C) 2022, 2023 JWP Consulting GK
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
"""Test workspace app rules."""
import pytest
from faker import Faker

from projectify.corporate.services.stripe import customer_cancel_subscription
from projectify.lib.auth import validate_perm
from projectify.user.models import User
from projectify.user.services.internal import user_create
from projectify.workspace.models.const import WorkspaceUserRoles
from projectify.workspace.models.section import (
    Section,
)
from projectify.workspace.models.task import Task
from projectify.workspace.models.workspace import Workspace
from projectify.workspace.models.workspace_board import WorkspaceBoard
from projectify.workspace.models.workspace_user import WorkspaceUser
from projectify.workspace.services.chat_message import chat_message_create
from projectify.workspace.services.label import label_create
from projectify.workspace.services.section import (
    section_create,
)
from projectify.workspace.services.sub_task import sub_task_create
from projectify.workspace.services.task import task_create
from projectify.workspace.services.workspace import (
    workspace_add_user,
)
from projectify.workspace.services.workspace_board import (
    workspace_board_create,
)
from projectify.workspace.services.workspace_user_invite import (
    workspace_user_invite_create,
)

from .. import (
    rules,
)


@pytest.fixture
def observer(workspace: Workspace, faker: Faker) -> WorkspaceUser:
    """Return an observer workspace user."""
    user = user_create(email=faker.email())
    return workspace_add_user(
        workspace=workspace,
        user=user,
        role=WorkspaceUserRoles.OBSERVER,
    )


@pytest.mark.django_db
class TestPredicates:
    """Test predicates."""

    def test_is_at_least_observer(
        self,
        workspace: Workspace,
        observer: WorkspaceUser,
    ) -> None:
        """Test is_at_least_observer."""
        # In the beginning the user is owner
        assert rules.is_at_least_observer(observer.user, workspace)

    def test_is_at_least_observer_unrelated_workspace(
        self,
        observer: WorkspaceUser,
        unrelated_workspace: Workspace,
    ) -> None:
        """Test is_at_least_observer with other workspace."""
        assert not rules.is_at_least_observer(
            observer.user, unrelated_workspace
        )

    def test_is_at_least_member(
        self,
        workspace: Workspace,
        observer: WorkspaceUser,
    ) -> None:
        """Test is_at_least_member."""
        assert not rules.is_at_least_member(observer.user, workspace)
        observer.assign_role(WorkspaceUserRoles.MEMBER)
        assert rules.is_at_least_member(observer.user, workspace)

    def test_is_at_least_member_unrelated_workspace(
        self,
        unrelated_workspace: Workspace,
        observer: WorkspaceUser,
    ) -> None:
        """Test is_at_least_member with other workspace."""
        assert not rules.is_at_least_member(observer.user, unrelated_workspace)

    def test_is_at_least_maintainer(
        self,
        workspace: Workspace,
        observer: WorkspaceUser,
    ) -> None:
        """Test is_at_least_maintainer."""
        assert not rules.is_at_least_maintainer(observer.user, workspace)
        observer.assign_role(WorkspaceUserRoles.MAINTAINER)
        assert rules.is_at_least_maintainer(observer.user, workspace)

    def test_is_at_least_maintainer_unrelated_workspace(
        self,
        unrelated_workspace: Workspace,
        observer: WorkspaceUser,
    ) -> None:
        """Test is_at_least_maintainer with other workspace."""
        assert not rules.is_at_least_maintainer(
            observer.user, unrelated_workspace
        )

    def test_is_at_least_owner(
        self,
        workspace: Workspace,
        observer: WorkspaceUser,
    ) -> None:
        """Test is_at_least_owner."""
        assert not rules.is_at_least_owner(observer.user, workspace)
        observer.assign_role(WorkspaceUserRoles.OWNER)
        assert rules.is_at_least_owner(observer.user, workspace)

    def test_is_at_least_owner_unrelated_workspace(
        self,
        observer: WorkspaceUser,
        unrelated_workspace: Workspace,
    ) -> None:
        """Test is_at_least_owner with other workspace."""
        assert not rules.is_at_least_owner(observer.user, unrelated_workspace)


@pytest.mark.django_db
class TestTrialRules:
    """
    Test trial conditions.

    User role shouldn't matter, only how many objects have been created.
    """

    @pytest.fixture(autouse=True)
    def patch_conditions(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """
        Patch trial_conditions to be easier to test.

        We go down to allowing one or two of each.
        """
        monkeypatch.setattr(
            "projectify.workspace.selectors.quota.trial_conditions",
            {
                "ChatMessage": 1,
                "Label": 1,
                "SubTask": 1,
                "Task": 1,
                "TaskLabel": 1,
                "WorkspaceBoard": 1,
                "Section": 1,
                # We need at least one user to use the workspace at all
                "WorkspaceUserAndInvite": 2,
            },
        )

    def test_create_chat_message(
        self,
        task: Task,
        user: User,
        workspace_user: WorkspaceUser,
        workspace: Workspace,
    ) -> None:
        """Assert 1 chat messages can not be created."""
        assert validate_perm("workspace.create_chat_message", user, workspace)
        customer_cancel_subscription(customer=workspace.customer)
        assert validate_perm("workspace.create_chat_message", user, workspace)
        chat_message_create(
            who=workspace_user.user, task=task, text="hello world"
        )
        assert not validate_perm(
            "workspace.create_chat_message",
            user,
            workspace,
            raise_exception=False,
        )

    def test_create_label(
        self,
        user: User,
        workspace_user: WorkspaceUser,
        workspace: Workspace,
    ) -> None:
        """Assert only 1 labels can be created."""
        assert validate_perm("workspace.create_label", user, workspace)
        customer_cancel_subscription(customer=workspace.customer)
        assert validate_perm("workspace.create_label", user, workspace)
        label_create(
            workspace=workspace,
            name="label",
            color=0,
            who=workspace_user.user,
        )
        assert not validate_perm(
            "workspace.create_label",
            user,
            workspace,
            raise_exception=False,
        )

    def test_create_sub_task(
        self,
        user: User,
        workspace_user: WorkspaceUser,
        workspace: Workspace,
        task: Task,
    ) -> None:
        """Assert only 1 sub task can be created."""
        assert validate_perm("workspace.create_sub_task", user, workspace)
        customer_cancel_subscription(customer=workspace.customer)
        assert validate_perm("workspace.create_sub_task", user, workspace)
        sub_task_create(
            task=task, title="sub task", who=workspace_user.user, done=False
        )
        assert not validate_perm(
            "workspace.create_sub_task",
            user,
            workspace,
            raise_exception=False,
        )

    def test_create_task(
        self,
        user: User,
        workspace_user: WorkspaceUser,
        section: Section,
        workspace: Workspace,
    ) -> None:
        """Assert only 1 task can be created."""
        assert validate_perm("workspace.create_task", user, workspace)
        customer_cancel_subscription(customer=workspace.customer)
        assert validate_perm("workspace.create_task", user, workspace)
        task_create(
            section=section,
            title="task title",
            who=workspace_user.user,
        )
        assert not validate_perm(
            "workspace.create_task",
            user,
            workspace,
            raise_exception=False,
        )

    def test_create_workspace_board(
        self,
        user: User,
        workspace_user: WorkspaceUser,
        workspace: Workspace,
    ) -> None:
        """Assert only 1 workspace board can be created."""
        assert validate_perm(
            "workspace.create_workspace_board", user, workspace
        )
        customer_cancel_subscription(customer=workspace.customer)
        assert validate_perm(
            "workspace.create_workspace_board", user, workspace
        )
        workspace_board_create(
            workspace=workspace,
            title="workspace board",
            who=workspace_user.user,
        )
        assert not validate_perm(
            "workspace.create_workspace_board",
            user,
            workspace,
            raise_exception=False,
        )

    def test_create_section(
        self,
        user: User,
        workspace_user: WorkspaceUser,
        workspace_board: WorkspaceBoard,
        workspace: Workspace,
    ) -> None:
        """Assert only 100 sections can be created."""
        assert validate_perm(
            "workspace.create_section",
            user,
            workspace,
        )
        customer_cancel_subscription(customer=workspace.customer)
        assert validate_perm(
            "workspace.create_section",
            user,
            workspace,
        )
        section_create(
            workspace_board=workspace_board,
            title="section",
            who=workspace_user.user,
        )
        assert not validate_perm(
            "workspace.create_section",
            user,
            workspace,
            raise_exception=False,
        )

    def test_workspace_user_and_invite_limit(
        self,
        user: User,
        workspace_user: WorkspaceUser,
        workspace: Workspace,
        faker: Faker,
        unrelated_user: User,
    ) -> None:
        """Assert only one more workspace user can be invited or added."""
        count = workspace.users.count()
        assert count == 1
        # Test both permissons
        assert validate_perm(
            "workspace.create_workspace_user", user, workspace
        )
        assert validate_perm(
            "workspace.create_workspace_user_invite", user, workspace
        )
        customer_cancel_subscription(customer=workspace.customer)
        assert validate_perm(
            "workspace.create_workspace_user", user, workspace
        )
        assert validate_perm(
            "workspace.create_workspace_user_invite", user, workspace
        )
        # Assume workspace_user_invite_create handles creating an invite and potential user creation
        invite = workspace_user_invite_create(
            workspace=workspace,
            email_or_user=faker.email(),
            who=workspace_user.user,
        )
        assert workspace.users.count() == count
        assert not validate_perm(
            "workspace.create_workspace_user",
            user,
            workspace,
            raise_exception=False,
        )
        assert not validate_perm(
            "workspace.create_workspace_user_invite",
            user,
            workspace,
            raise_exception=False,
        )
        # Back to allowed, now add
        invite.delete()
        assert validate_perm(
            "workspace.create_workspace_user", user, workspace
        )
        assert validate_perm(
            "workspace.create_workspace_user_invite", user, workspace
        )
        workspace_user_invite_create(
            workspace=workspace,
            who=workspace_user.user,
            email_or_user=unrelated_user,
        )
        assert workspace.users.count() == count + 1

        # Now forbidden again
        assert not validate_perm(
            "workspace.create_workspace_user",
            user,
            workspace,
            raise_exception=False,
        )
        assert not validate_perm(
            "workspace.create_workspace_user_invite",
            user,
            workspace,
            raise_exception=False,
        )
