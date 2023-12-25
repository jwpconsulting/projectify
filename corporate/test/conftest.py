"""Corporate conftest."""

import pytest
from faker import Faker

from corporate.models import Customer
from corporate.models.custom_code import CustomCode
from corporate.services.custom_code import custom_code_create
from corporate.services.customer import (
    customer_activate_subscription,
)
from user.models import User
from workspace.models.workspace import Workspace
from workspace.models.workspace_user import WorkspaceUser
from workspace.selectors.workspace_user import (
    workspace_user_find_for_workspace,
)
from workspace.services.workspace import workspace_create


@pytest.fixture
def stripe_publishable_key(faker: Faker) -> str:
    """Return a convincing looking stripe publishable key."""
    key: str = faker.hexify(
        "pk_test_^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^"
    )
    return key


@pytest.fixture
def stripe_secret_key(faker: Faker) -> str:
    """Return a convincing looking stripe secret key."""
    key: str = faker.hexify(
        "sk_test_^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^"
    )
    return key


@pytest.fixture
def stripe_price_object(faker: Faker) -> str:
    """Return a convincing looking stripe price object."""
    key: str = faker.hexify("price_^^^^^^^^^^^^^^^^^^^^^^^^")
    return key


@pytest.fixture
def stripe_endpoint_secret(faker: Faker) -> str:
    """Return a convincing looking stripe endpoint secret."""
    key: str = faker.hexify(
        "whsec_^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^"
    )
    return key


@pytest.fixture
def workspace(user: User, faker: Faker) -> Workspace:
    """Create a workspace."""
    return workspace_create(
        owner=user,
        title=faker.numerify("Corporate conftest workspace #####"),
    )


@pytest.fixture
def workspace_user(user: User, workspace: Workspace) -> WorkspaceUser:
    """Create a workspace user."""
    workspace_user = workspace_user_find_for_workspace(
        workspace=workspace, user=user
    )
    assert workspace_user
    return workspace_user


@pytest.fixture
def unpaid_customer(workspace: Workspace) -> Customer:
    """Create customer."""
    return workspace.customer


@pytest.fixture
def stripe_customer_id(faker: Faker) -> str:
    """Return a convincing stripe customer id."""
    stripe_customer_id: str = faker.bothify("stripe_###???###")
    return stripe_customer_id


@pytest.fixture
def paid_customer(
    unpaid_customer: Customer, stripe_customer_id: str
) -> Customer:
    """Create customer."""
    customer_activate_subscription(
        customer=unpaid_customer,
        stripe_customer_id=stripe_customer_id,
    )
    return unpaid_customer


@pytest.fixture
def custom_code(superuser: User) -> CustomCode:
    """Create a working custom code."""
    return custom_code_create(
        who=superuser, seats=20, prefix="i-am-a-test-custom-code"
    )
