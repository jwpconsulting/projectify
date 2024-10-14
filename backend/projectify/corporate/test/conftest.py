# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2022, 2023 JWP Consulting GK
"""Corporate conftest."""

import pytest
from faker import Faker

from projectify.user.models import User
from projectify.workspace.models.team_member import TeamMember
from projectify.workspace.models.workspace import Workspace
from projectify.workspace.selectors.team_member import (
    team_member_find_for_workspace,
)
from projectify.workspace.services.workspace import workspace_create

from ..models import Customer
from ..models.coupon import Coupon
from ..services.coupon import coupon_create
from ..services.stripe import customer_activate_subscription


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
def team_member(user: User, workspace: Workspace) -> TeamMember:
    """Create a team member."""
    team_member = team_member_find_for_workspace(
        workspace=workspace, user=user
    )
    assert team_member
    return team_member


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
        seats=1337,
    )
    return unpaid_customer


@pytest.fixture
def coupon(superuser: User) -> Coupon:
    """Create a working coupon."""
    return coupon_create(who=superuser, seats=20, prefix="i-am-a-test-coupon")
