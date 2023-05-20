"""Corporate conftest."""
from django.contrib.auth.models import (
    AbstractBaseUser,
)

import pytest

from workspace import factory as workspace_factory
from workspace import models as workspace_models

from .. import (
    factory,
    models,
)


@pytest.fixture
def workspace() -> workspace_models.Workspace:
    """Create workspace."""
    workspace: workspace_models.Workspace = (
        workspace_factory.WorkspaceFactory.create()
    )
    return workspace


@pytest.fixture
def customer(workspace: workspace_models.Workspace) -> models.Customer:
    """Create customer."""
    customer: models.Customer = factory.CustomerFactory.create(
        workspace=workspace
    )
    return customer


@pytest.fixture
def unpaid_customer(workspace: workspace_models.Workspace) -> models.Customer:
    """Create unpaid customer."""
    customer: models.Customer = factory.CustomerFactory.create(
        workspace=workspace,
        subscription_status=models.CustomerSubscriptionStatus.UNPAID,
    )
    return customer


@pytest.fixture
def workspace_user_unpaid_customer(
    user: AbstractBaseUser,
    unpaid_customer: models.Customer,
    workspace: workspace_models.Workspace,
) -> workspace_models.WorkspaceUser:
    """Create workspace user for unpaid customer workspace."""
    workspace_user: workspace_models.WorkspaceUser = (
        workspace_factory.WorkspaceUserFactory.create(
            user=user,
            workspace=workspace,
            role=workspace_models.WorkspaceUserRoles.OWNER,
        )
    )
    return workspace_user


@pytest.fixture
def workspace_user_customer(
    user: AbstractBaseUser,
    customer: models.Customer,
    workspace: workspace_models.Workspace,
) -> workspace_models.WorkspaceUser:
    """Create workspace user for paid customer workspace."""
    workspace_user: workspace_models.WorkspaceUser = (
        workspace_factory.WorkspaceUserFactory.create(
            user=user,
            workspace=workspace,
            role=workspace_models.WorkspaceUserRoles.OWNER,
        )
    )
    return workspace_user
