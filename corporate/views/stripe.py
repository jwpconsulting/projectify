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

from corporate.selectors.customer import (
    customer_find_by_stripe_customer_id,
    customer_find_by_uuid,
)
from corporate.services.customer import (
    customer_activate_subscription,
    customer_cancel_subscription,
    customer_update_seats,
)

endpoint_secret = settings.STRIPE_ENDPOINT_SECRET

logger = logging.getLogger(__name__)


def handle_session_completed(event: stripe.Event) -> bool:
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
    return True


def handle_subscription_updated(event: stripe.Event) -> bool:
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
    return True


def handle_payment_failure(event: stripe.Event) -> bool:
    """Handle Stripe invoice.payment_failed."""
    invoice = event["data"]["object"]
    if invoice.next_payment_attempt is not None:
        return True

    stripe_customer_id = invoice.customer
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
    return True


@csrf_exempt
def stripe_webhook(request: HttpRequest) -> HttpResponse:
    """Handle Stripe Webhooks."""
    payload = request.body
    sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
    event: stripe.Event

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError:
        # Invalid payload
        logger.exception("Invalid payload")
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        # Invalid signature
        logger.exception("Invalid signature")
        return HttpResponse(status=400)

    # Handle events
    dispatch = {
        "checkout.session.completed": handle_session_completed,
        "customer.subscription.updated": handle_subscription_updated,
        "invoice.payment_failed": handle_payment_failure,
    }

    if event.type in dispatch.keys():
        handler_response = dispatch[event.type](event)
        if handler_response:
            # If we can successfully handled the event
            return HttpResponse(status=200)
        else:
            logger.warning("Failed to handle event %s", event.type)
            return HttpResponse(status=400)
    else:
        logger.warning("Unhandled event type %s", event.type)
        return HttpResponse(status=400)
