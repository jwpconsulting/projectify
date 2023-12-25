"""Test custom code services."""
from django.core.exceptions import PermissionDenied

import pytest
from rest_framework import serializers

from corporate.models.custom_code import CustomCode
from corporate.models.customer import Customer
from corporate.services.custom_code import (
    custom_code_create,
    custom_code_redeem,
)
from corporate.services.customer import customer_check_active_for_workspace
from user.models import User
from workspace.models.workspace_user import WorkspaceUser
from workspace.services.workspace import workspace_create

pytestmark = pytest.mark.django_db


class TestCustomCodeCreate:
    """Test custom code creation."""

    def test_authorization(self, user: User, superuser: User) -> None:
        """Test that superusers can create codes, but no regular user."""
        seats = 20
        with pytest.raises(PermissionDenied):
            custom_code_create(who=user, seats=seats)
        custom_code_create(who=superuser, seats=seats)

    def test_code_is_unique(self, superuser: User) -> None:
        """Test that codes will not collide."""
        seats = 10
        code1 = custom_code_create(who=superuser, seats=seats, prefix="asd")
        code2 = custom_code_create(who=superuser, seats=seats, prefix="asd")
        assert code1.code != code2.code


class TestCustomCodeRedeem:
    """Test redeeming custom codes."""

    def test_invalid_code(self, workspace_user: WorkspaceUser) -> None:
        """Make sure nothing bad happens with an invalid code."""
        assert (
            customer_check_active_for_workspace(
                workspace=workspace_user.workspace
            )
            == "trial"
        )
        with pytest.raises(serializers.ValidationError) as error:
            custom_code_redeem(
                who=workspace_user.user,
                code="i-do-not-exist",
                workspace=workspace_user.workspace,
            )
        assert error.match("No custom code is available")
        assert (
            customer_check_active_for_workspace(
                workspace=workspace_user.workspace
            )
            == "trial"
        )

    def test_redeem_twice_different_workspace(
        self, custom_code: CustomCode, workspace_user: WorkspaceUser
    ) -> None:
        """Make sure we can't redeem a code twice."""
        user = workspace_user.user
        assert (
            customer_check_active_for_workspace(
                workspace=workspace_user.workspace
            )
            == "trial"
        )
        custom_code_redeem(
            who=user,
            code=custom_code.code,
            workspace=workspace_user.workspace,
        )
        assert (
            customer_check_active_for_workspace(
                workspace=workspace_user.workspace
            )
            == "full"
        )
        workspace = workspace_create(title="other workspace", owner=user)
        with pytest.raises(serializers.ValidationError) as error:
            custom_code_redeem(
                who=user,
                code="i-do-not-exist",
                workspace=workspace,
            )
        assert error.match("No custom code is available")
        assert (
            customer_check_active_for_workspace(
                workspace=workspace_user.workspace
            )
            == "full"
        )

    def test_redeem_different_codes_same_workspace(
        self,
        custom_code: CustomCode,
        workspace_user: WorkspaceUser,
        superuser: User,
    ) -> None:
        """Make sure we can't redeem two codes for a workspace."""
        workspace = workspace_user.workspace
        other_custom_code = custom_code_create(who=superuser, seats=1337)
        user = workspace_user.user
        assert (
            customer_check_active_for_workspace(workspace=workspace) == "trial"
        )
        custom_code_redeem(
            who=user,
            code=custom_code.code,
            workspace=workspace,
        )
        assert (
            customer_check_active_for_workspace(workspace=workspace) == "full"
        )
        with pytest.raises(serializers.ValidationError) as error:
            custom_code_redeem(
                who=user,
                code=other_custom_code.code,
                workspace=workspace,
            )
        assert error.match("already been used for this workspace")
        assert (
            customer_check_active_for_workspace(workspace=workspace) == "full"
        )

    def test_redeem_paid(
        self,
        workspace_user: WorkspaceUser,
        custom_code: CustomCode,
        paid_customer: Customer,
    ) -> None:
        """Ensure we can't redeem for an already paid workspace."""
        workspace = paid_customer.workspace
        with pytest.raises(serializers.ValidationError) as error:
            custom_code_redeem(
                who=workspace_user.user,
                code=custom_code.code,
                workspace=workspace,
            )
        assert error.match("already has an active subscription")
