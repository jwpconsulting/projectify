"""Test workspace app rules."""
import pytest
from faker import Faker

from corporate.models import CustomerSubscriptionStatus
from user.services.user import user_create
from workspace.models.const import WorkspaceUserRoles
from workspace.models.workspace import Workspace
from workspace.models.workspace_user import WorkspaceUser
from workspace.services.workspace import workspace_add_user

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

    def test_belongs_to_active_workspace(
        self,
        workspace: Workspace,
        observer: WorkspaceUser,
    ) -> None:
        """Test belongs_to_active_workspace."""
        # Active
        assert rules.belongs_to_active_workspace(
            observer.user,
            workspace,
        )
        # Inactive
        workspace.customer.subscription_status = (
            CustomerSubscriptionStatus.CANCELLED
        )
        assert not rules.belongs_to_active_workspace(
            observer.user,
            workspace,
        )

    @pytest.mark.xfail(
        reason="Workspaces should not exist without customers. Consider "
        "deleting this test"
    )
    def test_belongs_to_active_workspace_no_customer(
        self,
        workspace: Workspace,
        observer: WorkspaceUser,
    ) -> None:
        """Test belongs_to_active_workspace."""
        # The workspace fixture creates an active customer so we have to delete
        # it
        workspace.customer.delete()
        # The attribute has to be evicted by refreshing from db
        workspace.refresh_from_db()
        assert not rules.belongs_to_active_workspace(
            observer.user,
            workspace,
        )

    def test_belongs_to_active_workspace_unrelated_workspace(
        self,
        unrelated_workspace: Workspace,
        observer: WorkspaceUser,
    ) -> None:
        """Test belongs_to_active_workspace with other workspace."""
        assert not rules.belongs_to_active_workspace(
            observer.user,
            unrelated_workspace,
        )
