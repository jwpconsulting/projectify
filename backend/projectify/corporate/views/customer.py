# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Copyright (C) 2023-2024 JWP Consulting GK
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
"""Corporate views."""
import logging
from uuid import UUID

from django.utils.translation import gettext_lazy as _

from drf_spectacular.utils import extend_schema
from rest_framework import (
    exceptions,
    serializers,
)
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView

from projectify.lib.error_schema import DeriveSchema

from ..selectors.customer import customer_find_by_workspace_uuid
from ..serializers import CustomerSerializer
from ..services.customer import (
    create_billing_portal_session_for_customer,
    customer_create_stripe_checkout_session,
)

logger = logging.getLogger(__name__)


class WorkspaceCustomerRetrieve(APIView):
    """Retrieve customer for a workspace."""

    @extend_schema(
        responses={200: CustomerSerializer},
    )
    def get(self, request: Request, workspace_uuid: UUID) -> Response:
        """Handle GET."""
        user = request.user
        customer = customer_find_by_workspace_uuid(
            who=user,
            workspace_uuid=workspace_uuid,
        )
        if customer is None:
            raise exceptions.NotFound(
                _("No customer found for this workspace uuid")
            )
        serializer = CustomerSerializer(instance=customer)
        return Response(status=HTTP_200_OK, data=serializer.data)


# RPC
class WorkspaceCheckoutSessionCreate(APIView):
    """Create a checkout session given a workspace."""

    class WorkspaceCheckoutSessionCreateInputSerializer(
        serializers.Serializer
    ):
        """Accept a number of seats to be added into checkout."""

        seats = serializers.IntegerField(min_value=1)

    class WorkspaceCheckoutSessionCreateOutputSerializer(
        serializers.Serializer
    ):
        """Return the url to a checkout session."""

        # The original GraphQL mutation would also return an id. I believe this
        # was only needed if a stripe url is constructed client side
        url = serializers.URLField()

    @extend_schema(
        request=WorkspaceCheckoutSessionCreateInputSerializer,
        responses={
            200: WorkspaceCheckoutSessionCreateOutputSerializer,
            400: DeriveSchema,
        },
    )
    def post(self, request: Request, workspace_uuid: UUID) -> Response:
        """Handle POST."""
        customer = customer_find_by_workspace_uuid(
            workspace_uuid=workspace_uuid,
            who=request.user,
        )
        if customer is None:
            raise exceptions.NotFound(
                _("No customer found for this workspace uuid")
            )
        serializer = self.WorkspaceCheckoutSessionCreateInputSerializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        session = customer_create_stripe_checkout_session(
            customer=customer,
            who=request.user,
            seats=serializer.validated_data["seats"],
        )
        output_serializer = (
            self.WorkspaceCheckoutSessionCreateOutputSerializer(
                instance=session
            )
        )
        return Response(data=output_serializer.data, status=HTTP_200_OK)


class WorkspaceBillingPortalSessionCreate(APIView):
    """Create a billing portal session given a workspace."""

    class WorkspaceBillingPortalSessionCreateOutputSerializer(
        serializers.Serializer
    ):
        """Return the url to a billing portal session."""

        url = serializers.URLField()

    @extend_schema(
        request=None,
        responses={200: WorkspaceBillingPortalSessionCreateOutputSerializer},
    )
    def post(self, request: Request, workspace_uuid: UUID) -> Response:
        """Handle POST."""
        customer = customer_find_by_workspace_uuid(
            workspace_uuid=workspace_uuid, who=request.user
        )
        if customer is None:
            raise exceptions.NotFound(
                _("No customer found for this workspace uuid")
            )
        session = create_billing_portal_session_for_customer(
            who=request.user, customer=customer
        )
        output_serializer = (
            self.WorkspaceBillingPortalSessionCreateOutputSerializer(
                instance=session
            )
        )
        return Response(data=output_serializer.data, status=HTTP_200_OK)
