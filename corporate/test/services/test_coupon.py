# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Copyright (C) 2023 JWP Consulting GK
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
"""Test coupon services."""
from django.core.exceptions import PermissionDenied

import pytest
from rest_framework import serializers

from corporate.models.coupon import Coupon
from corporate.models.customer import Customer
from corporate.services.coupon import (
    coupon_create,
    coupon_redeem,
)
from corporate.services.customer import customer_check_active_for_workspace
from user.models import User
from workspace.models.workspace_user import WorkspaceUser
from workspace.services.workspace import workspace_create

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

    def test_invalid_code(self, workspace_user: WorkspaceUser) -> None:
        """Make sure nothing bad happens with an invalid code."""
        assert (
            customer_check_active_for_workspace(
                workspace=workspace_user.workspace
            )
            == "trial"
        )
        with pytest.raises(serializers.ValidationError) as error:
            coupon_redeem(
                who=workspace_user.user,
                code="i-do-not-exist",
                workspace=workspace_user.workspace,
            )
        assert error.match("No coupon is available")
        assert (
            customer_check_active_for_workspace(
                workspace=workspace_user.workspace
            )
            == "trial"
        )

    def test_redeem_twice_different_workspace(
        self, coupon: Coupon, workspace_user: WorkspaceUser
    ) -> None:
        """Make sure we can't redeem a code twice."""
        user = workspace_user.user
        assert (
            customer_check_active_for_workspace(
                workspace=workspace_user.workspace
            )
            == "trial"
        )
        coupon_redeem(
            who=user,
            code=coupon.code,
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
            coupon_redeem(
                who=user,
                code="i-do-not-exist",
                workspace=workspace,
            )
        assert error.match("No coupon is available")
        assert (
            customer_check_active_for_workspace(
                workspace=workspace_user.workspace
            )
            == "full"
        )

    def test_redeem_different_codes_same_workspace(
        self,
        coupon: Coupon,
        workspace_user: WorkspaceUser,
        superuser: User,
    ) -> None:
        """Make sure we can't redeem two codes for a workspace."""
        workspace = workspace_user.workspace
        other_coupon = coupon_create(who=superuser, seats=1337)
        user = workspace_user.user
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
        workspace_user: WorkspaceUser,
        coupon: Coupon,
        paid_customer: Customer,
    ) -> None:
        """Ensure we can't redeem for an already paid workspace."""
        workspace = paid_customer.workspace
        with pytest.raises(serializers.ValidationError) as error:
            coupon_redeem(
                who=workspace_user.user,
                code=coupon.code,
                workspace=workspace,
            )
        assert error.match("already has an active subscription")
