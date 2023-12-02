"""Test workspace app rules."""
from django.contrib.auth.models import (
    AbstractBaseUser,
)

import pytest

from corporate import models as corporate_models
from workspace.services.workspace import workspace_add_user

from .. import (
    models,
    rules,
)


@pytest.fixture
def observer(
    workspace: models.Workspace, user: AbstractBaseUser
) -> models.WorkspaceUser:
    """Return an observer workspace user."""
    return workspace_add_user(
        workspace=workspace,
        user=user,
        role=models.WorkspaceUserRoles.OBSERVER,
    )


@pytest.mark.django_db
class TestPredicates:
    """Test predicates."""

    def test_is_at_least_observer(
        self,
        user: AbstractBaseUser,
        workspace: models.Workspace,
        observer: models.WorkspaceUser,
    ) -> None:
        """Test is_at_least_observer."""
        # In the beginning the user is owner
        assert rules.is_at_least_observer(user, workspace)

    def test_is_at_least_observer_unrelated_workspace(
        self,
        user: AbstractBaseUser,
        unrelated_workspace: models.Workspace,
    ) -> None:
        """Test is_at_least_observer with other workspace."""
        assert not rules.is_at_least_observer(user, unrelated_workspace)

    def test_is_at_least_member(
        self,
        user: AbstractBaseUser,
        workspace: models.Workspace,
        observer: models.WorkspaceUser,
    ) -> None:
        """Test is_at_least_member."""
        assert not rules.is_at_least_member(user, workspace)
        observer.assign_role(models.WorkspaceUserRoles.MEMBER)
        assert rules.is_at_least_member(user, workspace)

    def test_is_at_least_member_unrelated_workspace(
        self,
        user: AbstractBaseUser,
        unrelated_workspace: models.Workspace,
        observer: models.WorkspaceUser,
    ) -> None:
        """Test is_at_least_member with other workspace."""
        assert not rules.is_at_least_member(user, unrelated_workspace)

    def test_is_at_least_maintainer(
        self,
        user: AbstractBaseUser,
        workspace: models.Workspace,
        observer: models.WorkspaceUser,
    ) -> None:
        """Test is_at_least_maintainer."""
        assert not rules.is_at_least_maintainer(user, workspace)
        observer.assign_role(models.WorkspaceUserRoles.MAINTAINER)
        assert rules.is_at_least_maintainer(user, workspace)

    def test_is_at_least_maintainer_unrelated_workspace(
        self, user: AbstractBaseUser, unrelated_workspace: models.Workspace
    ) -> None:
        """Test is_at_least_maintainer with other workspace."""
        assert not rules.is_at_least_maintainer(user, unrelated_workspace)

    def test_is_at_least_owner(
        self,
        user: AbstractBaseUser,
        workspace: models.Workspace,
        observer: models.WorkspaceUser,
    ) -> None:
        """Test is_at_least_owner."""
        assert not rules.is_at_least_owner(user, workspace)
        observer.assign_role(models.WorkspaceUserRoles.OWNER)
        assert rules.is_at_least_owner(user, workspace)

    def test_is_at_least_owner_unrelated_workspace(
        self,
        user: AbstractBaseUser,
        unrelated_workspace: models.Workspace,
    ) -> None:
        """Test is_at_least_owner with other workspace."""
        assert not rules.is_at_least_owner(user, unrelated_workspace)

    def test_belongs_to_active_workspace(
        self,
        user: AbstractBaseUser,
        workspace: models.Workspace,
        observer: models.WorkspaceUser,
    ) -> None:
        """Test belongs_to_active_workspace."""
        # Active
        assert rules.belongs_to_active_workspace(
            user,
            workspace,
        )
        # Inactive
        workspace.customer.subscription_status = (
            corporate_models.CustomerSubscriptionStatus.CANCELLED
        )
        assert not rules.belongs_to_active_workspace(
            user,
            workspace,
        )

    def test_belongs_to_active_workspace_no_customer(
        self,
        user: AbstractBaseUser,
        workspace: models.Workspace,
        observer: models.WorkspaceUser,
    ) -> None:
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

    def test_belongs_to_active_workspace_unrelated_workspace(
        self,
        user: AbstractBaseUser,
        unrelated_workspace: models.Workspace,
        observer: models.WorkspaceUser,
    ) -> None:
        """Test belongs_to_active_workspace with other workspace."""
        assert not rules.belongs_to_active_workspace(
            user,
            unrelated_workspace,
        )
