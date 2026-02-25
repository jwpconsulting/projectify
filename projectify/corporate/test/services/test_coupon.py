# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023 JWP Consulting GK
"""Test coupon services."""

import pytest
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

from projectify.user.models import User
from projectify.workspace.models.team_member import TeamMember
from projectify.workspace.services.workspace import workspace_create

from ...models.coupon import Coupon
from ...models.customer import Customer
from ...selectors.customer import customer_check_active_for_workspace
from ...services.coupon import coupon_create, coupon_redeem

pytestmark = pytest.mark.django_db


class TestCouponCreate:
    """Test coupon creation."""

    def test_authorization(self, user: User, superuser: User) -> None:
        """Test that superusers can create codes, but no regular user."""
        seats = 20
        with pytest.raises(PermissionDenied):
            coupon_create(who=user, seats=seats)
        coupon_create(who=superuser, seats=seats)

    def test_code_is_unique(self, superuser: User) -> None:
        """Test that codes will not collide."""
        seats = 10
        code1 = coupon_create(who=superuser, seats=seats, prefix="asd")
        code2 = coupon_create(who=superuser, seats=seats, prefix="asd")
        assert code1.code != code2.code


class TestCouponRedeem:
    """Test redeeming coupons."""

    def test_invalid_code(
        self,
        team_member: TeamMember,
        unpaid_customer: Customer,
    ) -> None:
        """Make sure nothing bad happens with an invalid code."""
        assert (
            customer_check_active_for_workspace(
                workspace=team_member.workspace
            )
            == "trial"
        )
        with pytest.raises(serializers.ValidationError) as error:
            coupon_redeem(
                who=team_member.user,
                code="i-do-not-exist",
                workspace=team_member.workspace,
            )
        assert error.match("No coupon is available")
        assert (
            customer_check_active_for_workspace(
                workspace=team_member.workspace
            )
            == "trial"
        )

    def test_redeem_twice_different_workspace(
        self,
        coupon: Coupon,
        team_member: TeamMember,
        unpaid_customer: Customer,
    ) -> None:
        """Make sure we can't redeem a code twice."""
        user = team_member.user
        assert (
            customer_check_active_for_workspace(
                workspace=team_member.workspace
            )
            == "trial"
        )
        coupon_redeem(
            who=user,
            code=coupon.code,
            workspace=team_member.workspace,
        )
        assert (
            customer_check_active_for_workspace(
                workspace=team_member.workspace
            )
            == "full"
        )
        workspace = workspace_create(title="other workspace", owner=user)
        with pytest.raises(serializers.ValidationError) as error:
            coupon_redeem(
                who=user,
                code="i-do-not-exist",
                workspace=workspace,
            )
        assert error.match("No coupon is available")
        assert (
            customer_check_active_for_workspace(
                workspace=team_member.workspace
            )
            == "full"
        )

    def test_redeem_different_codes_same_workspace(
        self,
        coupon: Coupon,
        team_member: TeamMember,
        superuser: User,
        unpaid_customer: Customer,
    ) -> None:
        """Make sure we can't redeem two codes for a workspace."""
        workspace = team_member.workspace
        other_coupon = coupon_create(who=superuser, seats=1337)
        user = team_member.user
        assert (
            customer_check_active_for_workspace(workspace=workspace) == "trial"
        )
        coupon_redeem(
            who=user,
            code=coupon.code,
            workspace=workspace,
        )
        assert (
            customer_check_active_for_workspace(workspace=workspace) == "full"
        )
        with pytest.raises(serializers.ValidationError) as error:
            coupon_redeem(
                who=user,
                code=other_coupon.code,
                workspace=workspace,
            )
        assert error.match("already been used for this workspace")
        assert (
            customer_check_active_for_workspace(workspace=workspace) == "full"
        )

    def test_redeem_paid(
        self,
        team_member: TeamMember,
        coupon: Coupon,
        paid_customer: Customer,
    ) -> None:
        """Ensure we can't redeem for an already paid workspace."""
        workspace = paid_customer.workspace
        with pytest.raises(serializers.ValidationError) as error:
            coupon_redeem(
                who=team_member.user,
                code=coupon.code,
                workspace=workspace,
            )
        assert error.match("already has an active subscription")
