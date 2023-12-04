"""Services for customer model."""
import logging

from corporate.models import Customer, CustomerSubscriptionStatus
from corporate.types import WorkspaceFeatures
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
    customer.stripe_customer_id = stripe_customer_id
    customer.subscription_status = CustomerSubscriptionStatus.ACTIVE
    customer.save()


# TODO permissions needed?
def customer_update_seats(*, customer: Customer, seats: int) -> None:
    """Update the number of seats for a customer."""
    # TODO Check why returning None is required
    if customer.seats == seats:
        logger.warning(
            "Customer %s set the same number of seats (%d) as before",
            str(customer.uuid),
            seats,
        )
        return None
    customer.seats = seats
    customer.save()


# TODO permissions needed?
# Since this will be called by Stripe, the who could be an explicit Stripe
# identifier
def customer_cancel_subscription(*, customer: Customer) -> None:
    """Cancel a customer's subscription."""
    customer.subscription_status = CustomerSubscriptionStatus.CANCELLED
    customer.save()


# TODO permissions needed?
# TODO check whether a workspace is in trial, then check further conditions
# TODO rename customer_check_workspace_features
def customer_check_active_for_workspace(
    *, workspace: Workspace
) -> WorkspaceFeatures:
    """Check if a customer is active for a given workspace."""
    try:
        customer = workspace.customer
    except Customer.DoesNotExist:
        raise ValueError(f"No customer found for workspace {workspace}")
    match customer.subscription_status:
        case CustomerSubscriptionStatus.ACTIVE:
            return "full"
        case CustomerSubscriptionStatus.CUSTOM:
            return "full"
        case CustomerSubscriptionStatus.UNPAID:
            logger.warning("Customer for workspace %s is inactive", workspace)
            return "trial"
        case CustomerSubscriptionStatus.CANCELLED:
            logger.warning("Customer for workspace %s is inactive", workspace)
            return "inactive"
        case status:
            raise ValueError(f"Unknown status {status}")
