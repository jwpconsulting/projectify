"""Services for customer model."""
import logging

from corporate.models import Customer, CustomerSubscriptionStatus
from projectify.utils import validate_perm
from user.models import User
from workspace.models.workspace import Workspace

logger = logging.getLogger(__name__)


def customer_create(
    *, who: User, workspace: Workspace, seats: int
) -> Customer:
    """Create a customer."""
    validate_perm("corporate.can_create_customer", who, workspace)
    return Customer.objects.create(workspace=workspace, seats=seats)


# TODO permissions needed?
def customer_activate_subscription(
    *, customer: Customer, stripe_customer_id: str
) -> None:
    """Active a subscription for a customer."""
    # TODO:
    # The two following method can be refactored as well.
    customer.assign_stripe_customer_id(stripe_customer_id)
    customer.activate_subscription()


# TODO permissions needed?
def customer_update_seats(*, customer: Customer, seats: int) -> None:
    """Update the number of seats for a customer."""
    # TODO refactor the following method into here
    customer.set_number_of_seats(seats)


# TODO permissions needed?
def customer_cancel_subscription(*, customer: Customer) -> None:
    """Cancel a customer's subscription."""
    # TODO the following method should be refactored into here
    customer.cancel_subscription()


# TODO permissions needed?
def customer_check_active_for_workspace(*, workspace: Workspace) -> bool:
    """Check if a customer is active for a given workspace."""
    try:
        customer = workspace.customer
    except Customer.DoesNotExist:
        logger.warning("No customer found for workspace %s", workspace)
        return False
    match customer.subscription_status:
        case CustomerSubscriptionStatus.ACTIVE:
            return True
        case CustomerSubscriptionStatus.CUSTOM:
            return True
        case _:
            logger.warning("Customer for workspace %s is inactive", workspace)
            return False
