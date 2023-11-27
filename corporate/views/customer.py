"""Corporate views."""
import logging

from rest_framework import (
    generics,
)

from corporate.models import Customer, CustomerQuerySet
from corporate.serializers import CustomerSerializer

logger = logging.getLogger(__name__)


class WorkspaceCustomerRetrieve(
    generics.RetrieveAPIView[
        Customer,
        CustomerQuerySet,
        CustomerSerializer,
    ]
):
    """Retrieve customer for a workspace."""

    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def get_queryset(self) -> CustomerQuerySet:
        """Filter by request user."""
        user = self.request.user
        return self.queryset.filter_by_user(user)

    def get_object(self) -> Customer:
        """Get customer."""
        return self.get_queryset().get_by_workspace_uuid(
            self.kwargs["workspace_uuid"]
        )
