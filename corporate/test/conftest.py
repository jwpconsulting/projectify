"""Corporate conftest."""

import pytest
from faker import Faker

from corporate.models import Customer
from corporate.services.customer import (
    customer_activate_subscription,
    customer_create,
)
from user.models import User
from workspace.models.const import WorkspaceUserRoles
from workspace.models.workspace import Workspace
from workspace.models.workspace_user import WorkspaceUser
from workspace.services.workspace import workspace_add_user


@pytest.fixture
def workspace(faker: Faker) -> Workspace:
    """Create a workspace."""
    return Workspace.objects.create(title=faker.company())


@pytest.fixture
def workspace_user(user: User, workspace: Workspace) -> WorkspaceUser:
    """Create a workspace user."""
    return workspace_add_user(
        workspace=workspace,
        user=user,
        role=WorkspaceUserRoles.OWNER,
    )


@pytest.fixture
def unpaid_customer(
    workspace_user: WorkspaceUser, workspace: Workspace, faker: Faker
) -> Customer:
    """Create customer."""
    return customer_create(
        who=workspace_user.user,
        workspace=workspace,
        seats=faker.pyint(min_value=1, max_value=98),
    )


@pytest.fixture
def paid_customer(
    unpaid_customer: Customer,
    faker: Faker,
) -> Customer:
    """Create customer."""
    customer_activate_subscription(
        customer=unpaid_customer,
        stripe_customer_id=faker.bothify("stripe_###???###"),
    )
    return unpaid_customer
