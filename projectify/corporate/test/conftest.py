# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Copyright (C) 2022, 2023 JWP Consulting GK
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""Corporate conftest."""

import pytest
from faker import Faker

from projectify.corporate.models import Customer
from projectify.corporate.models.coupon import Coupon
from projectify.corporate.services.coupon import coupon_create
from projectify.corporate.services.customer import (
    customer_activate_subscription,
)
from projectify.user.models import User
from projectify.workspace.models.workspace import Workspace
from projectify.workspace.models.workspace_user import WorkspaceUser
from projectify.workspace.selectors.workspace_user import (
    workspace_user_find_for_workspace,
)
from projectify.workspace.services.workspace import workspace_create


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
def coupon(superuser: User) -> Coupon:
    """Create a working coupon."""
    return coupon_create(who=superuser, seats=20, prefix="i-am-a-test-coupon")
