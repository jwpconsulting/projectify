"""Corporate app urls."""
from django.urls import (
    path,
)

from . import (
    views,
)


app_name = "corporate"

urlpatterns = [
    path(
        "workspace/<uuid:workspace_uuid>/customer",
        views.WorkspaceCustomerRetrieve.as_view(),
        name="workspace-customer",
    ),
    path("stripe-webhook/", views.stripe_webhook, name="stripe-webhook"),
]
