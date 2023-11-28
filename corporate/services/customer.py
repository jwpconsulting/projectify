"""Services for customer model."""
from corporate.models import Customer


def customer_activate_subscription(
    *, customer: Customer, stripe_customer_id: str
) -> None:
    """Active a subscription for a customer."""
    # TODO:
    # The two following method can be refactored as well.
    customer.assign_stripe_customer_id(stripe_customer_id)
    customer.activate_subscription()


def customer_update_seats(*, customer: Customer, seats: int) -> None:
    """Update the number of seats for a customer."""
    # TODO refactor the following method into here
    customer.set_number_of_seats(seats)


def customer_cancel_subscription(*, customer: Customer) -> None:
    """Cancel a customer's subscription."""
    # TODO the following method should be refactored into here
    customer.cancel_subscription()
