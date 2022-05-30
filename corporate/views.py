"""Corporate views."""
import logging

from django.conf import (
    settings,
)
from django.http import (
    HttpResponse,
)
from django.views.decorators.csrf import (
    csrf_exempt,
)

import stripe


endpoint_secret = settings.STRIPE_ENDPOINT_SECRET

logger = logging.getLogger(__name__)


@csrf_exempt
def stripe_webhook(request):
    """Handle Stripe Webhooks."""
    payload = request.body
    sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
    event = None

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

    # Handle the event
    if event.type == "checkout.session.completed":
        pass
    else:
        logger.warning("Unhandled event type %s", event.type)
        print("Unhandled event type {}".format(event.type))

    return HttpResponse(status=200)
