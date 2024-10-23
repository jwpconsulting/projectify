# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2022, 2023 JWP Consulting GK
"""Test workspace app rules."""

import pytest
from faker import Faker

from projectify.corporate.services.stripe import customer_cancel_subscription
from projectify.lib.auth import validate_perm
from projectify.user.models import User
from projectify.user.services.internal import user_create
from projectify.workspace.models.const import TeamMemberRoles
from projectify.workspace.models.project import Project
from projectify.workspace.models.section import (
    Section,
)
from projectify.workspace.models.task import Task
from projectify.workspace.models.team_member import TeamMember
from projectify.workspace.models.workspace import Workspace
from projectify.workspace.services.chat_message import chat_message_create
from projectify.workspace.services.label import label_create
from projectify.workspace.services.project import (
    project_create,
)
from projectify.workspace.services.section import (
    section_create,
)
from projectify.workspace.services.sub_task import sub_task_create
from projectify.workspace.services.task import task_create
from projectify.workspace.services.team_member_invite import (
    team_member_invite_create,
)
from projectify.workspace.services.workspace import (
    workspace_add_user,
)

from .. import (
    rules,
)


@pytest.fixture
def observer(workspace: Workspace, faker: Faker) -> TeamMember:
    """Return an observer team member."""
    user = user_create(email=faker.email())
    return workspace_add_user(
        workspace=workspace,
        user=user,
        role=TeamMemberRoles.OBSERVER,
    )


@pytest.mark.django_db
class TestPredicates:
    """Test predicates."""

    def test_is_at_least_observer(
        self,
        workspace: Workspace,
        observer: TeamMember,
    ) -> None:
        """Test is_at_least_observer."""
        # In the beginning the user is owner
        assert rules.is_at_least_observer(observer.user, workspace)

    def test_is_at_least_observer_unrelated_workspace(
        self,
        observer: TeamMember,
        unrelated_workspace: Workspace,
    ) -> None:
        """Test is_at_least_observer with other workspace."""
        assert not rules.is_at_least_observer(
            observer.user, unrelated_workspace
        )

    def test_is_at_least_contributor(
        self,
        workspace: Workspace,
        observer: TeamMember,
    ) -> None:
        """Test is_at_least_contributor."""
        assert not rules.is_at_least_contributor(observer.user, workspace)
        observer.assign_role(TeamMemberRoles.CONTRIBUTOR)
        assert rules.is_at_least_contributor(observer.user, workspace)

    def test_is_at_least_contributor_unrelated_workspace(
        self,
        unrelated_workspace: Workspace,
        observer: TeamMember,
    ) -> None:
        """Test is_at_least_contributor with other workspace."""
        assert not rules.is_at_least_contributor(
            observer.user, unrelated_workspace
        )

    def test_is_at_least_maintainer(
        self,
        workspace: Workspace,
        observer: TeamMember,
    ) -> None:
        """Test is_at_least_maintainer."""
        assert not rules.is_at_least_maintainer(observer.user, workspace)
        observer.assign_role(TeamMemberRoles.MAINTAINER)
        assert rules.is_at_least_maintainer(observer.user, workspace)

    def test_is_at_least_maintainer_unrelated_workspace(
        self,
        unrelated_workspace: Workspace,
        observer: TeamMember,
    ) -> None:
        """Test is_at_least_maintainer with other workspace."""
        assert not rules.is_at_least_maintainer(
            observer.user, unrelated_workspace
        )

    def test_is_at_least_owner(
        self,
        workspace: Workspace,
        observer: TeamMember,
    ) -> None:
        """Test is_at_least_owner."""
        assert not rules.is_at_least_owner(observer.user, workspace)
        observer.assign_role(TeamMemberRoles.OWNER)
        assert rules.is_at_least_owner(observer.user, workspace)

    def test_is_at_least_owner_unrelated_workspace(
        self,
        observer: TeamMember,
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
                "Project": 1,
                "Section": 1,
                # We need at least one user to use the workspace at all
                "TeamMemberAndInvite": 2,
            },
        )

    def test_create_chat_message(
        self,
        task: Task,
        user: User,
        team_member: TeamMember,
        workspace: Workspace,
    ) -> None:
        """Assert 1 chat messages can not be created."""
        assert validate_perm("workspace.create_chat_message", user, workspace)
        customer_cancel_subscription(customer=workspace.customer)
        assert validate_perm("workspace.create_chat_message", user, workspace)
        chat_message_create(
            who=team_member.user, task=task, text="hello world"
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
        team_member: TeamMember,
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
            who=team_member.user,
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
        team_member: TeamMember,
        workspace: Workspace,
        task: Task,
    ) -> None:
        """Assert only 1 sub task can be created."""
        assert validate_perm("workspace.create_sub_task", user, workspace)
        customer_cancel_subscription(customer=workspace.customer)
        assert validate_perm("workspace.create_sub_task", user, workspace)
        sub_task_create(
            task=task, title="sub task", who=team_member.user, done=False
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
        team_member: TeamMember,
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
            who=team_member.user,
        )
        assert not validate_perm(
            "workspace.create_task",
            user,
            workspace,
            raise_exception=False,
        )

    def test_create_project(
        self,
        user: User,
        team_member: TeamMember,
        workspace: Workspace,
    ) -> None:
        """Assert only 1 project can be created."""
        assert validate_perm("workspace.create_project", user, workspace)
        customer_cancel_subscription(customer=workspace.customer)
        assert validate_perm("workspace.create_project", user, workspace)
        project_create(
            workspace=workspace,
            title="project",
            who=team_member.user,
        )
        assert not validate_perm(
            "workspace.create_project",
            user,
            workspace,
            raise_exception=False,
        )

    def test_create_section(
        self,
        user: User,
        team_member: TeamMember,
        project: Project,
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
            project=project,
            title="section",
            who=team_member.user,
        )
        assert not validate_perm(
            "workspace.create_section",
            user,
            workspace,
            raise_exception=False,
        )

    def test_team_member_and_invite_limit(
        self,
        user: User,
        team_member: TeamMember,
        workspace: Workspace,
        faker: Faker,
        unrelated_user: User,
    ) -> None:
        """Assert only one more team member can be invited or added."""
        count = workspace.users.count()
        assert count == 1
        # Test both permissons
        assert validate_perm("workspace.create_team_member", user, workspace)
        assert validate_perm(
            "workspace.create_team_member_invite", user, workspace
        )
        customer_cancel_subscription(customer=workspace.customer)
        assert validate_perm("workspace.create_team_member", user, workspace)
        assert validate_perm(
            "workspace.create_team_member_invite", user, workspace
        )
        # Assume team_member_invite_create handles creating an invite and potential user creation
        invite = team_member_invite_create(
            workspace=workspace,
            email_or_user=faker.email(),
            who=team_member.user,
        )
        assert workspace.users.count() == count
        assert not validate_perm(
            "workspace.create_team_member",
            user,
            workspace,
            raise_exception=False,
        )
        assert not validate_perm(
            "workspace.create_team_member_invite",
            user,
            workspace,
            raise_exception=False,
        )
        # Back to allowed, now add
        invite.delete()
        assert validate_perm("workspace.create_team_member", user, workspace)
        assert validate_perm(
            "workspace.create_team_member_invite", user, workspace
        )
        team_member_invite_create(
            workspace=workspace,
            who=team_member.user,
            email_or_user=unrelated_user,
        )
        assert workspace.users.count() == count + 1

        # Now forbidden again
        assert not validate_perm(
            "workspace.create_team_member",
            user,
            workspace,
            raise_exception=False,
        )
        assert not validate_perm(
            "workspace.create_team_member_invite",
            user,
            workspace,
            raise_exception=False,
        )
