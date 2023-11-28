"""Corporate views."""
import logging
from uuid import UUID

from rest_framework import (
    generics,
    serializers,
)
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView

from corporate.models import Customer, CustomerQuerySet
from corporate.serializers import CustomerSerializer
from corporate.services.stripe import (
    create_billing_portal_session_for_workspace_uuid,
    stripe_checkout_session_create_for_workspace_uuid,
)

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


# RPC
class WorkspaceCheckoutSessionCreate(APIView):
    """Create a checkout session given a workspace."""

    class InputSerializer(serializers.Serializer):
        """Accept a number of seats to be added into checkout."""

        seats = serializers.IntegerField(
            min_value=1,
        )

    class OutputSerializer(serializers.Serializer):
        """Return the url to a checkout session."""

        # The original GraphQL mutation would also return an id. I believe this
        # was only needed if a stripe url is constructed client side
        url = serializers.URLField()

    def post(self, request: Request, workspace_uuid: UUID) -> Response:
        """Handle POST."""
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        session = stripe_checkout_session_create_for_workspace_uuid(
            workspace_uuid=workspace_uuid,
            who=request.user,
            seats=data["seats"],
        )
        output_serializer = self.OutputSerializer(instance=session)
        return Response(data=output_serializer.data, status=HTTP_200_OK)


class WorkspaceBillingPortalSessionCreate(APIView):
    """Create a billing portal session given a workspace."""

    class OutputSerializer(serializers.Serializer):
        """Return the url to a billing portal session."""

        url = serializers.URLField()

    def post(self, request: Request, workspace_uuid: UUID) -> Response:
        """Handle POST."""
        session = create_billing_portal_session_for_workspace_uuid(
            who=request.user,
            workspace_uuid=workspace_uuid,
        )
        output_serializer = self.OutputSerializer(instance=session)
        return Response(data=output_serializer.data, status=HTTP_200_OK)
