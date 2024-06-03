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
from collections.abc import Callable, Mapping
from typing import Any, Literal, Optional, Union
from uuid import UUID

from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import (
    csrf_exempt,
)

import stripe
from drf_spectacular.utils import extend_schema
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

from projectify.lib.settings import get_settings

from ..lib.stripe import stripe_client
from ..models.customer import Customer
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


def _deserialize_stripe_customer(
    customer: Union[None, str, stripe.Customer],
) -> Optional[str]:
    """Get customer id string from various .customer properties."""
    match customer:
        case None:
            return None
        case str():
            return customer
        case stripe.Customer():
            return customer.id


def _get_customer_from_metadata(session: stripe.checkout.Session) -> Customer:
    """Try to get customer from metadata."""
    metadata = session.metadata
    if metadata is None:
        raise serializers.ValidationError({"metadata": _("Expected metadata")})
    customer_uuid_raw: Optional[str] = metadata.get("customer_uuid")

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
    return customer


def handle_session_completed(session: stripe.checkout.Session) -> None:
    """Handle Stripe checkout.session.completed."""
    stripe_customer_id = _deserialize_stripe_customer(session.customer)

    if stripe_customer_id is None:
        logger.warn(
            "A stripe checkout session was completed, but no customer was given"
        )
        return

    customer = _get_customer_from_metadata(session)

    # We'd like to make sure that we have the actual line items, for the most
    # recent session that they have created, not seats that we store
    # in database
    line_items = session.list_line_items()

    match line_items.data:
        case [item]:
            pass
        case []:
            raise serializers.ValidationError(
                {"items": _("Expected 1 line item")}
            )
        case _:
            raise serializers.ValidationError(
                {"items": _("There are too many line items")}
            )

    seats = item.quantity
    if seats is None:
        raise serializers.ValidationError(
            {"line_items.data.quantity": _("Expected value")}
        )

    customer_activate_subscription(
        customer=customer,
        stripe_customer_id=stripe_customer_id,
        seats=seats,
    )


def _get_customer_from_stripe_customer(
    stripe_customer: Union[None, str, stripe.Customer],
) -> Optional[Customer]:
    """Get our customer using their customer id."""
    stripe_customer_id = _deserialize_stripe_customer(stripe_customer)
    if stripe_customer_id is None:
        return None
    customer = customer_find_by_stripe_customer_id(
        stripe_customer_id=stripe_customer_id
    )
    if customer is None:
        raise serializers.ValidationError(
            {"customer": _("Could not find customer for this id")}
        )
    return customer


def handle_subscription_updated(subscription: stripe.Subscription) -> None:
    """Handle Stripe customer.subscription.updated."""
    customer = _get_customer_from_stripe_customer(subscription.customer)
    if customer is None:
        logger.warn(
            "customer.subscription.updated event received, but no customer provded"
        )
        return

    client = stripe_client()
    items = client.subscription_items.list(
        params={"subscription": subscription.id},
    ).data

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


def handle_payment_failure(invoice: stripe.Invoice) -> None:
    """Handle Stripe invoice.payment_failed."""
    customer = _get_customer_from_stripe_customer(invoice.customer)
    if customer is None:
        logger.warn(
            "customer.subscription.updated event received, but no customer provded"
        )
        return

    # If there is a next payment attempt scheduled, we should not cancel
    # immediately
    if invoice.next_payment_attempt is not None:
        logger.info("Payment failed, but will try charging %s again", customer)
        return

    customer_cancel_subscription(customer=customer)
    logger.info(
        "Customer %s has failed to renew payment for their account.", customer
    )


def handle_subscription_cancelled(subscription: stripe.Subscription) -> None:
    """Handle Stripe customer_subscription.cancelled."""
    # TODO check subscription.status
    # https://docs.stripe.com/api/subscriptions/object#subscription_object-status
    customer = _get_customer_from_stripe_customer(subscription.customer)
    if customer is None:
        logger.warn(
            "customer.subscription.cancelled event received, "
            "but no customer provided"
        )
        return

    customer_cancel_subscription(customer=customer)
    logger.info(
        "Customer %s has failed to renew payment for their account.", customer
    )


# Handle events
dispatch: Mapping[str, Callable[[Any], None]] = {
    "checkout.session.completed": handle_session_completed,
    "customer.subscription.updated": handle_subscription_updated,
    "invoice.payment_failed": handle_payment_failure,
    "customer.subscription.deleted": handle_subscription_cancelled,
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


def _handle_event(
    event: stripe.Event,
) -> Literal["ok", "bad_request", "internal_server_error"]:
    """Dispatch to event handler and return HttpResponse."""
    event_type: str = event.type

    handler = dispatch.get(event_type)

    if handler is None:
        logger.warning("Unhandled event type %s", event_type)
        return "ok"

    try:
        handler(event["data"]["object"])
    except serializers.ValidationError as e:
        logger.exception("Invalid input for event %s", event_type)
        raise e
    except Exception:
        logger.exception("Error encountered for %s", event_type)
        return "internal_server_error"
    return "ok"


@extend_schema(
    # TODO?
    request=None,
    responses={
        200: None,
        400: None,
    },
)
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
            pass

    result = _handle_event(event)
    match result:
        case "bad_request":
            return Response(status=HTTP_400_BAD_REQUEST)
        case "internal_server_error":
            return Response(status=HTTP_500_INTERNAL_SERVER_ERROR)
        case "ok":
            return Response(status=HTTP_200_OK)
