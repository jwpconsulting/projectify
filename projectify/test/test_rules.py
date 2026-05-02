# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2022-2026 JWP Consulting GK
"""Test workspace app rules."""

import pytest
from faker import Faker

from projectify.corporate.services.stripe import customer_cancel_subscription
from projectify.settings.base import Base
from projectify.user.models import User
from projectify.user.services.internal import user_create
from projectify.workspace.const import TeamMemberRoles
from projectify.workspace.models import Project, Section, TeamMember, Workspace
from projectify.workspace.services.project import project_create
from projectify.workspace.services.section import section_create
from projectify.workspace.services.task import task_create
from projectify.workspace.services.team_member import team_member_change_role
from projectify.workspace.services.team_member_invite import (
    team_member_invite_create,
)
from projectify.workspace.services.workspace import workspace_add_user

from .. import rules
from ..lib.auth import validate_perm


@pytest.fixture
def observer(workspace: Workspace, faker: Faker) -> TeamMember:
    """Return an observer team member."""
    user = user_create(email=faker.email())
    return workspace_add_user(
        workspace=workspace, user=user, role=TeamMemberRoles.OBSERVER
    )


@pytest.mark.django_db
class TestPredicates:
    """Test predicates."""

    def test_is_at_least_observer(self, observer: TeamMember) -> None:
        """Test is_at_least_observer."""
        workspace = observer.workspace
        # In the beginning the user is owner
        assert rules.is_at_least_observer(observer.user, workspace)

    def test_is_at_least_observer_unrelated_workspace(
        self, observer: TeamMember, unrelated_workspace: Workspace
    ) -> None:
        """Test is_at_least_observer with other workspace."""
        assert not rules.is_at_least_observer(
            observer.user, unrelated_workspace
        )

    def test_is_at_least_contributor(
        self, observer: TeamMember, user: User
    ) -> None:
        """Test is_at_least_contributor."""
        workspace = observer.workspace
        assert not rules.is_at_least_contributor(observer.user, workspace)
        team_member_change_role(
            team_member=observer, who=user, role=TeamMemberRoles.CONTRIBUTOR
        )
        workspace.refresh_from_db()
        assert rules.is_at_least_contributor(observer.user, workspace)

    def test_is_at_least_contributor_unrelated_workspace(
        self, unrelated_workspace: Workspace, observer: TeamMember
    ) -> None:
        """Test is_at_least_contributor with other workspace."""
        assert not rules.is_at_least_contributor(
            observer.user, unrelated_workspace
        )

    def test_is_at_least_maintainer(
        self, observer: TeamMember, user: User
    ) -> None:
        """Test is_at_least_maintainer."""
        workspace = observer.workspace
        assert not rules.is_at_least_maintainer(observer.user, workspace)
        team_member_change_role(
            team_member=observer, who=user, role=TeamMemberRoles.MAINTAINER
        )
        workspace.refresh_from_db()
        assert rules.is_at_least_maintainer(observer.user, workspace)

    def test_is_at_least_maintainer_unrelated_workspace(
        self, unrelated_workspace: Workspace, observer: TeamMember
    ) -> None:
        """Test is_at_least_maintainer with other workspace."""
        assert not rules.is_at_least_maintainer(
            observer.user, unrelated_workspace
        )

    def test_is_at_least_owner(self, observer: TeamMember, user: User) -> None:
        """Test is_at_least_owner."""
        workspace = observer.workspace
        assert not rules.is_at_least_owner(observer.user, workspace)
        team_member_change_role(
            team_member=observer, who=user, role=TeamMemberRoles.OWNER
        )
        workspace.refresh_from_db()
        assert rules.is_at_least_owner(observer.user, workspace)

    def test_is_at_least_owner_unrelated_workspace(
        self, observer: TeamMember, unrelated_workspace: Workspace
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
                "Task": 1,
                "Project": 1,
                "Section": 1,
                # We need at least one user to use the workspace at all
                "TeamMemberAndInvite": 2,
            },
        )

    def test_no_billing_integration(
        self, settings: Base, team_member: TeamMember, section: Section
    ) -> None:
        """Assert that with no billing, the 1 task limit becomes inactive."""
        user = team_member.user
        workspace = team_member.workspace
        assert validate_perm("workspace.create_task", user, workspace)
        customer_cancel_subscription(customer=workspace.customer)
        assert validate_perm("workspace.create_task", user, workspace)
        task_create(section=section, title="task title", who=user)
        assert not validate_perm(
            "workspace.create_task", user, workspace, raise_exception=False
        )
        settings.STRIPE_CONFIG = None
        assert validate_perm(
            "workspace.create_task", user, workspace, raise_exception=False
        )
        task_create(section=section, title="task title", who=user)

    def test_create_task(
        self, team_member: TeamMember, section: Section
    ) -> None:
        """Assert only 1 task can be created."""
        workspace = section.project.workspace
        user = team_member.user
        assert validate_perm("workspace.create_task", user, workspace)
        customer_cancel_subscription(customer=workspace.customer)
        assert validate_perm("workspace.create_task", user, workspace)
        task_create(section=section, title="task title", who=user)
        assert not validate_perm(
            "workspace.create_task", user, workspace, raise_exception=False
        )

    def test_create_project(self, team_member: TeamMember) -> None:
        """Assert only 1 project can be created."""
        user = team_member.user
        workspace = team_member.workspace
        assert validate_perm("workspace.create_project", user, workspace)
        customer_cancel_subscription(customer=workspace.customer)
        assert validate_perm("workspace.create_project", user, workspace)
        project_create(workspace=workspace, title="project", who=user)
        assert not validate_perm(
            "workspace.create_project", user, workspace, raise_exception=False
        )

    def test_create_section(
        self, team_member: TeamMember, project: Project, workspace: Workspace
    ) -> None:
        """Assert only 100 sections can be created."""
        user = team_member.user
        assert validate_perm("workspace.create_section", user, workspace)
        customer_cancel_subscription(customer=workspace.customer)
        assert validate_perm("workspace.create_section", user, workspace)
        section_create(project=project, title="section", who=user)
        assert not validate_perm(
            "workspace.create_section", user, workspace, raise_exception=False
        )

    def test_team_member_and_invite_limit(
        self, team_member: TeamMember, faker: Faker, unrelated_user: User
    ) -> None:
        """Assert only one more team member can be invited or added."""
        user = team_member.user
        workspace = team_member.workspace
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

        # Current user can't remove or update themselves
        assert not validate_perm(
            "workspace.delete_team_member",
            user,
            team_member,
            raise_exception=False,
        )
        assert not validate_perm(
            "workspace.update_team_member_role",
            user,
            team_member,
            raise_exception=False,
        )
        # But they can change other things about themselves
        assert validate_perm("workspace.update_team_member", user, workspace)

        invite = team_member_invite_create(
            workspace=workspace, email_or_user=faker.email(), who=user
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
        new_team_member = team_member_invite_create(
            workspace=workspace, who=user, email_or_user=unrelated_user
        )
        assert isinstance(new_team_member, TeamMember)
        assert workspace.users.count() == count + 1
        assert user.has_perm("workspace.delete_team_member", new_team_member)
        assert user.has_perm("workspace.update_team_member", workspace)

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
