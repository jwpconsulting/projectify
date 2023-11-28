"""Corporate app customer model selectors."""

from typing import Optional
from uuid import UUID

from corporate.models import Customer


def customer_find_by_uuid(*, customer_uuid: UUID) -> Optional[Customer]:
    """Find a customer by UUID."""
    try:
        # The following method can be refactored in here
        return Customer.objects.get_by_uuid(customer_uuid)
    except Customer.DoesNotExist:
        return None


def customer_find_by_stripe_customer_id(
    *, stripe_customer_id: str
) -> Optional[Customer]:
    """Find a customer by stripe id."""
    try:
        # The following method can be refactored in here
        return Customer.objects.get_by_stripe_customer_id(stripe_customer_id)
    except Customer.DoesNotExist:
        return None
