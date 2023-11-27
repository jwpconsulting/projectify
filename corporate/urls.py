"""Corporate app urls."""
from django.urls import (
    path,
)

from corporate.views.customer import WorkspaceCustomerRetrieve
from corporate.views.stripe import stripe_webhook

app_name = "corporate"

urlpatterns = [
    path(
        "workspace/<uuid:workspace_uuid>/customer",
        WorkspaceCustomerRetrieve.as_view(),
        name="workspace-customer",
    ),
    path("stripe-webhook/", stripe_webhook, name="stripe-webhook"),
]
