"""Corporate app urls."""
from django.urls import (
    include,
    path,
)

from corporate.views.coupon import CouponRedeem
from corporate.views.customer import (
    WorkspaceBillingPortalSessionCreate,
    WorkspaceCheckoutSessionCreate,
    WorkspaceCustomerRetrieve,
)
from corporate.views.stripe import stripe_webhook

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
