"""Top level conftest module."""
import base64
import json

from django.core.files.uploadedfile import (
    SimpleUploadedFile,
)
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
def other_user():
    """Return another db user."""
    return UserFactory.create()


@pytest.fixture
def inactive_user():
    """Return an inactive db user."""
    return UserFactory.create(is_active=False)


@pytest.fixture
def graphql_query(client):
    """Return a client query fn without logged in user."""

    def func(*args, **kwargs):
        return json.loads(
            testing.graphql_query(
                *args,
                **kwargs,
                client=client,
                graphql_url=reverse("graphql"),
            ).content
        )

    return func


@pytest.fixture
def graphql_query_user(client, user):
    """Return a client query fn."""

    def func(*args, **kwargs):
        return json.loads(
            testing.graphql_query(
                *args,
                **kwargs,
                client=client,
                graphql_url=reverse("graphql"),
            ).content,
        )

    client.force_login(user)
    return func


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


@pytest.fixture
def png_image():
    """Return a simple png file."""
    return base64.b64decode(
        "iVBORw0KGgoAAAANSUhEUgAAACAAAAAgAgAAAAAcoT2JAAAABGdBTUEAAYagMeiWX\
        wAAAB9JREFUeJxjYAhd9R+M8TCIUMIAU4aPATMJH2OQuQcAvUl/gYsJiakAAAAASUVORK5\
        CYII="
    )


@pytest.fixture
def uploaded_file(png_image):
    """Return an UploadFile instance of the above png file."""
    return SimpleUploadedFile("test.png", png_image)
