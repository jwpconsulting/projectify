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
"""Callback views for Stripe."""
import logging
from typing import Literal, Union
from uuid import UUID

from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import (
    csrf_exempt,
)

import stripe
from rest_framework import serializers
from rest_framework.decorators import (
    api_view,
    permission_classes,
)
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_500_INTERNAL_SERVER_ERROR,
)
from stripe.checkout import Session

from projectify.corporate.lib.stripe import stripe_client
from projectify.lib.settings import get_settings

from ..selectors.customer import (
    customer_find_by_stripe_customer_id,
    customer_find_by_uuid,
)
from ..services.stripe import (
    customer_activate_subscription,
    customer_cancel_subscription,
    customer_update_seats,
)

logger = logging.getLogger(__name__)


def handle_session_completed(event: stripe.Event) -> None:
    """Handle Stripe checkout.session.completed."""
    session: Session = event["data"]["object"]

    if session.metadata is None:
        raise serializers.ValidationError({"metadata": _("Expected metadata")})
    customer_uuid_raw = session.metadata.get("customer_uuid")

    if customer_uuid_raw is None:
        raise serializers.ValidationError(
            {"metadata": {"customer_uuid": _("Expected value")}}
        )

    # XXX
    # Looks like a job for DRF serializers
    try:
        customer_uuid = UUID(customer_uuid_raw)
    except ValueError:
        raise serializers.ValidationError(
            {
                "metadata": {
                    "customer_uuid": _("Not a valid UUID {}").format(
                        customer_uuid_raw
                    )
                }
            }
        )

    customer = customer_find_by_uuid(customer_uuid=customer_uuid)

    if customer is None:
        raise serializers.ValidationError(
            {"metadata": {"customer_uuid": _("No customer for this uuid")}}
        )

    stripe_customer = session.customer
    match stripe_customer:
        case None:
            raise serializers.ValidationError(
                {"customer": _("Expected customer")},
            )
        case str():
            stripe_customer_id = stripe_customer
        case stripe.Customer():
            stripe_customer_id = stripe_customer.id

    customer_activate_subscription(
        customer=customer,
        stripe_customer_id=stripe_customer_id,
    )


def handle_subscription_updated(event: stripe.Event) -> None:
    """Handle Stripe customer.subscription.updated."""
    subscription: stripe.Subscription = event["data"]["object"]
    stripe_customer = subscription.customer
    match stripe_customer:
        case str():
            stripe_customer_id = stripe_customer
        case stripe.Customer():
            stripe_customer_id = stripe_customer.id

    customer = customer_find_by_stripe_customer_id(
        stripe_customer_id=stripe_customer_id
    )

    if customer is None:
        raise serializers.ValidationError(
            {"customer": _("Could not find customer for this id")}
        )
    items = subscription.items.data

    match items:
        case [item]:
            pass
        case []:
            raise serializers.ValidationError(
                {"items": _("Expected 1 subscription item")}
            )
        case _:
            raise serializers.ValidationError(
                {"items": _("There are too many subscription items")}
            )
    seats = item.quantity
    if seats is None:
        raise serializers.ValidationError(
            {"items": {"quantity": _("Expected quantity")}}
        )

    customer_update_seats(customer=customer, seats=seats)
    logger.info("Customer %s updated subscription: %s", customer, subscription)


def handle_payment_failure(event: stripe.Event) -> None:
    """Handle Stripe invoice.payment_failed."""
    invoice: stripe.Invoice = event["data"]["object"]

    # TODO should this be handled as some kind of error?
    if invoice.next_payment_attempt is not None:
        logger.warn(
            "next_payment_attempt was given for invoice.payment_failed: %s",
            invoice,
        )
        return

    match invoice.customer:
        case str() as stripe_customer_id:
            pass
        case stripe.Customer() as stripe_customer:
            stripe_customer_id = stripe_customer.id
        case None:
            raise serializers.ValidationError(
                {"customer": _("Expected a customer")}
            )

    customer = customer_find_by_stripe_customer_id(
        stripe_customer_id=stripe_customer_id
    )
    if customer is None:
        raise serializers.ValidationError(
            {"customer": _("No customer found for this id")}
        )
    customer_cancel_subscription(customer=customer)
    logger.info(
        "Customer %s has failed to renew payment for their account.", customer
    )


# Handle events
dispatch = {
    "checkout.session.completed": handle_session_completed,
    "customer.subscription.updated": handle_subscription_updated,
    "invoice.payment_failed": handle_payment_failure,
}


def _construct_event(
    payload: bytes, sig_header: str
) -> Union[stripe.Event, Literal["invalid_payload", "invalid_signature"]]:
    """Construct an event, and maybe return errors."""
    settings = get_settings()
    endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
    if endpoint_secret is None:
        raise ValueError("Expected STRIPE_ENDPOINT_SECRET")

    client = stripe_client()

    try:
        return client.construct_event(
            payload=payload,
            sig_header=sig_header,
            secret=endpoint_secret,
        )
    except ValueError:
        # Invalid payload
        logger.exception("Invalid payload")
        return "invalid_payload"
    except stripe.SignatureVerificationError:
        # Invalid signature
        logger.exception("Invalid signature")
        return "invalid_signature"


def _handle_event(event: stripe.Event) -> Response:
    """Dispatch to event handler and return HttpResponse."""
    event_type: str = event.type

    handler = dispatch.get(event_type)

    if handler is None:
        logger.warning("Unhandled event type %s", event_type)
        return Response(status=HTTP_400_BAD_REQUEST)

    try:
        handler(event)
    except serializers.ValidationError:
        logger.exception("Invalid input for event %s", event_type)
        return Response(status=HTTP_400_BAD_REQUEST)
    except Exception:
        logger.exception("Error encountered for %s", event_type)
        return Response(status=HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(status=HTTP_200_OK)


@csrf_exempt
@api_view(["POST"])
@permission_classes([AllowAny])
def stripe_webhook(request: Request) -> Response:
    """Construct event type using data coming from stripe."""
    payload = request.body
    sig_header = request.META["HTTP_STRIPE_SIGNATURE"]

    event = _construct_event(payload, sig_header)
    match event:
        case "invalid_payload":
            return Response(status=HTTP_400_BAD_REQUEST)
        case "invalid_signature":
            return Response(status=HTTP_400_BAD_REQUEST)
        case event:
            return _handle_event(event)
