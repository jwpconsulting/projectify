"""Top level conftest module."""
import base64
from unittest import (
    mock,
)

from django.contrib.auth.models import (
    AnonymousUser,
)
from django.core.files.uploadedfile import (
    SimpleUploadedFile,
)

import pytest

from projectify.schema import (
    schema,
)
from projectify.views import (
    RequestContext,
)
from user.factory import (
    SuperUserFactory,
    UserFactory,
    UserInviteFactory,
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
def user_invite():
    """Return a user invite."""
    return UserInviteFactory()


@pytest.fixture
def redeemed_user_invite(user):
    """Return a redeemed user invite."""
    return UserInviteFactory(redeemed=True, user=user, email=user.email)


def dict_from_execution_result(result):
    """Turn an execution result into a dict."""
    if result.errors:
        return {
            "data": result.data,
            "errors": result.errors,
        }
    return {
        "data": result.data,
    }


@pytest.fixture
def graphql_query():
    """Return a client query fn without logged in user."""

    def func(query, variables=None):
        result = schema.execute_sync(
            query,
            variable_values=variables,
            context_value=RequestContext(
                user=AnonymousUser(),
                session=mock.MagicMock(),
                META={},
            ),
        )
        return dict_from_execution_result(result)

    return func


@pytest.fixture
def graphql_query_user(user):
    """Return a client query fn."""

    def func(query, variables=None):
        result = schema.execute_sync(
            query,
            variable_values=variables,
            context_value=RequestContext(
                user=user,
                session=mock.MagicMock(),
                META={},
            ),
        )
        return dict_from_execution_result(result)

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
