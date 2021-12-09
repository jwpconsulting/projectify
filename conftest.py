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
    UserFactory,
)


@pytest.fixture
def user():
    """Return a db user."""
    return UserFactory.create()


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
