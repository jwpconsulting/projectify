"""Corporate conftest."""
import pytest

from workspace import factory as workspace_factory
from workspace import models as workspace_models

from .. import (
    factory,
    models,
)


@pytest.fixture
def customer():
    """Create customer."""
    return factory.CustomerFactory()


@pytest.fixture
def unpaid_customer():
    """Create unpaid customer."""
    customer = factory.CustomerFactory(
        subscription_status=models.Customer.SubscriptionStatus.UNPAID
    )
    return customer


@pytest.fixture
def workspace_user_unpaid_customer(user, unpaid_customer):
    """Create workspace user for unpaid customer workspace."""
    workspace = unpaid_customer.workspace
    return workspace_factory.WorkspaceUserFactory(
        user=user,
        workspace=workspace,
        role=workspace_models.WorkspaceUserRoles.OWNER,
    )


@pytest.fixture
def workspace_user_customer(user, customer):
    """Create workspace user for paid customer workspace."""
    workspace = customer.workspace
    return workspace_factory.WorkspaceUserFactory(
        user=user,
        workspace=workspace,
        role=workspace_models.WorkspaceUserRoles.OWNER,
    )
