"""Test workspace app rules."""
import pytest

from corporate import models as corporate_models

from .. import (
    factory,
    models,
    rules,
)


@pytest.fixture
def observer(workspace, user):
    """Return an observer workspace user."""
    return factory.WorkspaceUserFactory(
        workspace=workspace,
        user=user,
        role=models.WorkspaceUserRoles.OBSERVER,
    )


@pytest.mark.django_db
class TestPredicates:
    """Test predicates."""

    def test_is_at_least_observer(self, user, workspace, observer):
        """Test is_at_least_observer."""
        # In the beginning the user is owner
        assert rules.is_at_least_observer(user, workspace)

    def test_is_at_least_observer_other_workspace(self, user, other_workspace):
        """Test is_at_least_observer with other workspace."""
        assert not rules.is_at_least_observer(user, other_workspace)

    def test_is_at_least_member(self, user, workspace, observer):
        """Test is_at_least_member."""
        assert not rules.is_at_least_member(user, workspace)
        observer.assign_role(models.WorkspaceUserRoles.MEMBER)
        assert rules.is_at_least_member(user, workspace)

    def test_is_at_least_member_other_workspace(
        self, user, other_workspace, observer
    ):
        """Test is_at_least_member with other workspace."""
        assert not rules.is_at_least_member(user, other_workspace)

    def test_is_at_least_maintainer(self, user, workspace, observer):
        """Test is_at_least_maintainer."""
        assert not rules.is_at_least_maintainer(user, workspace)
        observer.assign_role(models.WorkspaceUserRoles.MAINTAINER)
        assert rules.is_at_least_maintainer(user, workspace)

    def test_is_at_least_maintainer_other_workspace(
        self, user, other_workspace
    ):
        """Test is_at_least_maintainer with other workspace."""
        assert not rules.is_at_least_maintainer(user, other_workspace)

    def test_is_at_least_owner(self, user, workspace, observer):
        """Test is_at_least_owner."""
        assert not rules.is_at_least_owner(user, workspace)
        observer.assign_role(models.WorkspaceUserRoles.OWNER)
        assert rules.is_at_least_owner(user, workspace)

    def test_is_at_least_owner_other_workspace(self, user, other_workspace):
        """Test is_at_least_owner with other workspace."""
        assert not rules.is_at_least_owner(user, other_workspace)

    def test_belongs_to_active_workspace(
        self,
        user,
        workspace,
        observer,
    ):
        """Test belongs_to_active_workspace."""
        # Active
        assert rules.belongs_to_active_workspace(
            user,
            workspace,
        )
        # Inactive
        workspace.customer.subscription_status = (
            corporate_models.Customer.SubscriptionStatus.CANCELLED
        )
        assert not rules.belongs_to_active_workspace(
            user,
            workspace,
        )

    def test_belongs_to_active_workspace_no_customer(
        self, user, workspace, observer
    ):
        """Test belongs_to_active_workspace."""
        # The workspace fixture creates an active customer so we have to delete
        # it
        workspace.customer.delete()
        # The attribute has to be evicted by refreshing from db
        workspace.refresh_from_db()
        assert not rules.belongs_to_active_workspace(
            user,
            workspace,
        )

    def test_belongs_to_active_workspace_other_workspace(
        self, user, other_workspace, observer
    ):
        """Test belongs_to_active_workspace with other workspace."""
        assert not rules.belongs_to_active_workspace(
            user,
            other_workspace,
        )
