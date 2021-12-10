"""Top level conftest module."""
import json

from django.urls import (
    reverse,
)

import pytest
from graphene_django.utils import (
    testing,
)

from user.factory import (
    SuperUserFactory,
    UserFactory,
)


@pytest.fixture
def user():
    """Return a db user."""
    return UserFactory.create()


@pytest.fixture
def superuser():
    """Return a db super user."""
    return SuperUserFactory.create()


@pytest.fixture
def inactive_user():
    """Return an inactive db user."""
    return UserFactory.create(is_active=False)


@pytest.fixture
def graphql_query(client):
    """Return a client query fn without logged in user."""

    def func(*args, **kwargs):
        return testing.graphql_query(
            *args,
            **kwargs,
            client=client,
            graphql_url=reverse("graphql"),
        )

    return func


@pytest.fixture
def graphql_query_user(client, user):
    """Return a client query fn."""

    def func(*args, **kwargs):
        return testing.graphql_query(
            *args,
            **kwargs,
            client=client,
            graphql_url=reverse("graphql"),
        )

    client.force_login(user)
    return func


@pytest.fixture
def json_loads():
    """Return json loads."""
    return json.loads


@pytest.fixture
def user_client(client, user):
    """Return logged in client."""
    client.force_login(user)
    return client


@pytest.fixture
def superuser_client(client, superuser):
    """Return logged in super user client."""
    client.force_login(superuser)
    return client
