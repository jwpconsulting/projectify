"""Corporate conftest."""
import pytest

from workspace import factory as workspace_factory
from workspace import models as workspace_models

from .. import (
    factory,
    models,
)


@pytest.fixture
def workspace():
    """Create workspace."""
    return workspace_factory.WorkspaceFactory()


@pytest.fixture
def customer(workspace):
    """Create customer."""
    return factory.CustomerFactory(workspace=workspace)


@pytest.fixture
def unpaid_customer(workspace):
    """Create unpaid customer."""
    return factory.CustomerFactory(
        workspace=workspace,
        subscription_status=models.CustomerSubscriptionStatus.UNPAID,
    )


@pytest.fixture
def workspace_user_unpaid_customer(user, unpaid_customer, workspace):
    """Create workspace user for unpaid customer workspace."""
    return workspace_factory.WorkspaceUserFactory(
        user=user,
        workspace=workspace,
        role=workspace_models.WorkspaceUserRoles.OWNER,
    )


@pytest.fixture
def workspace_user_customer(user, customer, workspace):
    """Create workspace user for paid customer workspace."""
    return workspace_factory.WorkspaceUserFactory(
        user=user,
        workspace=workspace,
        role=workspace_models.WorkspaceUserRoles.OWNER,
    )
