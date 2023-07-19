"""Corporate views."""
import logging

from django.conf import (
    settings,
)
from django.http import (
    HttpRequest,
    HttpResponse,
)
from django.views.decorators.csrf import (
    csrf_exempt,
)

from rest_framework import (
    generics,
)

import stripe

from . import (
    models,
    serializers,
)


endpoint_secret = settings.STRIPE_ENDPOINT_SECRET

logger = logging.getLogger(__name__)


class WorkspaceCustomerRetrieve(
    generics.RetrieveAPIView[
        models.Customer,
        models.CustomerQuerySet,
        serializers.CustomerSerializer,
    ]
):
    """Retrieve customer for a workspace."""

    queryset = models.Customer.objects.all()
    serializer_class = serializers.CustomerSerializer

    def get_queryset(self) -> models.CustomerQuerySet:
        """Filter by request user."""
        user = self.request.user
        return self.queryset.filter_by_user(user)

    def get_object(self) -> models.Customer:
        """Get customer."""
        return self.get_queryset().get_by_workspace_uuid(
            self.kwargs["workspace_uuid"]
        )


def handle_session_completed(event: stripe.Event) -> bool:
    """Handle Stripe checkout.session.completed."""
    session = event["data"]["object"]
    customer_uuid = session.metadata.customer_uuid
    customer = models.Customer.objects.get_by_uuid(customer_uuid)
    customer.assign_stripe_customer_id(session.customer)
    customer.activate_subscription()
    return True


def handle_subscription_updated(event: stripe.Event) -> bool:
    """Handle Stripe customer.subscription.updated."""
    subscription = event["data"]["object"]
    customer_id = subscription.customer
    customer = models.Customer.objects.get_by_stripe_customer_id(customer_id)
    customer.set_number_of_seats(subscription.quantity)
    logger.info("Customer %s updated subscription: %s", customer, subscription)
    return True


def handle_payment_failure(event: stripe.Event) -> bool:
    """Handle Stripe invoice.payment_failed."""
    invoice = event["data"]["object"]
    if invoice.next_payment_attempt is None:
        stripe_customer_id = invoice.customer
        customer = models.Customer.objects.get_by_stripe_customer_id(
            stripe_customer_id
        )
        customer.cancel_subscription()
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
