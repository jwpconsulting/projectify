# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023-2024 JWP Consulting GK
"""Corporate views."""

import logging
from uuid import UUID

from django.utils.translation import gettext_lazy as _

from rest_framework import exceptions, serializers
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView

from ..selectors.customer import customer_find_by_workspace_uuid
from ..services.customer import (
    create_billing_portal_session_for_customer,
    customer_create_stripe_checkout_session,
)

logger = logging.getLogger(__name__)


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
