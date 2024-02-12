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
"""Corporate app urls."""
from django.urls import (
    include,
    path,
)

from projectify.corporate.views.coupon import CouponRedeem
from projectify.corporate.views.customer import (
    WorkspaceBillingPortalSessionCreate,
    WorkspaceCheckoutSessionCreate,
    WorkspaceCustomerRetrieve,
)
from projectify.corporate.views.stripe import stripe_webhook

app_name = "corporate"

customer_url_patterns = (
    # Read
    path(
        "<uuid:workspace_uuid>/customer",
        WorkspaceCustomerRetrieve.as_view(),
        name="read",
    ),
    # RPC
    path(
        "<uuid:workspace_uuid>/create-checkout-session",
        WorkspaceCheckoutSessionCreate.as_view(),
        name="create-checkout-session",
    ),
    path(
        "<uuid:workspace_uuid>/create-billing-portal-session",
        WorkspaceBillingPortalSessionCreate.as_view(),
        name="create-billing-portal-session",
    ),
)

coupon_url_patterns = (
    # RPC
    path(
        "<uuid:workspace_uuid>/redeem-coupon",
        CouponRedeem.as_view(),
        name="redeem-coupon",
    ),
)

urlpatterns = [
    # Customer
    path("workspace/", include((customer_url_patterns, "customers"))),
    # Coupon
    path("workspace/", include((coupon_url_patterns, "coupons"))),
    # Stripe
    path("stripe-webhook/", stripe_webhook, name="stripe-webhook"),
]
