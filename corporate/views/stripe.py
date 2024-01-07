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
from uuid import UUID

from django.conf import (
    settings,
)
from django.http import (
    HttpRequest,
    HttpResponse,
)
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import (
    csrf_exempt,
)

import stripe
from rest_framework import serializers
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_500_INTERNAL_SERVER_ERROR,
)

from corporate.selectors.customer import (
    customer_find_by_stripe_customer_id,
    customer_find_by_uuid,
)
from corporate.services.customer import (
    customer_activate_subscription,
    customer_cancel_subscription,
    customer_update_seats,
)

logger = logging.getLogger(__name__)


endpoint_secret = settings.STRIPE_ENDPOINT_SECRET


def handle_session_completed(event: stripe.Event) -> None:
    """Handle Stripe checkout.session.completed."""
    session = event["data"]["object"]
    customer_uuid: UUID = session.metadata.customer_uuid
    stripe_customer_id: str = session.customer
    customer = customer_find_by_uuid(
        customer_uuid=customer_uuid,
    )
    if customer is None:
        raise serializers.ValidationError(
            {"metadata": {"customer_uuid": _("No customer for this uuid")}}
        )
    customer_activate_subscription(
        customer=customer,
        stripe_customer_id=stripe_customer_id,
    )


def handle_subscription_updated(event: stripe.Event) -> None:
    """Handle Stripe customer.subscription.updated."""
    subscription = event["data"]["object"]
    stripe_customer_id: str = subscription.customer
    customer = customer_find_by_stripe_customer_id(
        stripe_customer_id=stripe_customer_id
    )
    if customer is None:
        raise serializers.ValidationError(
            {"customer": _("Could not find customer for this id")}
        )
    seats: int = subscription.quantity
    customer_update_seats(customer=customer, seats=seats)
    logger.info("Customer %s updated subscription: %s", customer, subscription)


def handle_payment_failure(event: stripe.Event) -> None:
    """Handle Stripe invoice.payment_failed."""
    invoice = event["data"]["object"]

    # TODO should this be handled as some kind of error?
    if invoice.next_payment_attempt is not None:
        logger.warn(
            "next_payment_attempt was given for invoice.payment_failed: %s",
            invoice,
        )
        return

    stripe_customer_id: str = invoice.customer
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


# TODO Refactor this as a DRF view function so that we can get nicer
# errors
@csrf_exempt
def stripe_webhook(request: HttpRequest) -> HttpResponse:
    """Handle Stripe Webhooks."""
    payload = request.body
    sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
    event: stripe.Event

    try:
        event = stripe.Webhook.construct_event(
            payload=payload,
            sig_header=sig_header,
            secret=endpoint_secret,
        )
    except ValueError:
        # Invalid payload
        logger.exception("Invalid payload")
        return HttpResponse(status=HTTP_400_BAD_REQUEST)
    except stripe.error.SignatureVerificationError:
        # Invalid signature
        logger.exception("Invalid signature")
        return HttpResponse(status=HTTP_400_BAD_REQUEST)

    event_type: str = event.type

    handler = dispatch.get(event_type)

    if handler is None:
        logger.warning("Unhandled event type %s", event_type)
        return HttpResponse(status=HTTP_400_BAD_REQUEST)

    try:
        handler(event)
    except serializers.ValidationError:
        logger.exception("Invalid input for event %s", event_type)
        return HttpResponse(status=HTTP_400_BAD_REQUEST)
    except Exception:
        logger.exception("Error encountered for %s", event_type)
        return HttpResponse(status=HTTP_500_INTERNAL_SERVER_ERROR)

    return HttpResponse(status=HTTP_200_OK)
