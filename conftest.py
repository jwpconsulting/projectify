"""Top level conftest module."""
import base64
from typing import (
    Any,
    Dict,
    Mapping,
    Optional,
    Protocol,
)
from unittest import (
    mock,
)

from django.contrib.auth.models import (
    AbstractBaseUser,
    AnonymousUser,
)
from django.core.files.uploadedfile import (
    SimpleUploadedFile,
)
from django.test import (
    client,
)

import pytest
from rest_framework.test import (
    APIClient,
)
from strawberry.types.execution import (
    ExecutionResult,
)

from projectify.schema import (
    schema,
)
from projectify.views import (
    RequestContext,
)
from user import models as user_models
from user.factory import (
    SuperUserFactory,
    UserFactory,
    UserInviteFactory,
)


@pytest.fixture
def user() -> AbstractBaseUser:
    """Return a db user."""
    user: AbstractBaseUser = UserFactory.create()
    return user


@pytest.fixture
def superuser() -> AbstractBaseUser:
    """Return a db super user."""
    user: AbstractBaseUser = SuperUserFactory.create()
    return user


@pytest.fixture
def other_user() -> AbstractBaseUser:
    """Return another db user."""
    user: AbstractBaseUser = UserFactory.create()
    return user


@pytest.fixture
def inactive_user() -> AbstractBaseUser:
    """Return an inactive db user."""
    user: AbstractBaseUser = UserFactory.create(is_active=False)
    return user


@pytest.fixture
def user_invite() -> user_models.UserInvite:
    """Return a user invite."""
    user_invite: user_models.UserInvite = UserInviteFactory.create()
    return user_invite


@pytest.fixture
def redeemed_user_invite(user: user_models.User) -> user_models.UserInvite:
    """Return a redeemed user invite."""
    user_invite: user_models.UserInvite = UserInviteFactory.create(
        redeemed=True, user=user, email=user.email
    )
    return user_invite


Variables = Dict[str, Any]
ExecutionResultDict = Mapping[str, object]


class QueryMethod(Protocol):
    """Protocol for graphql conftest query helper."""

    def __call__(
        self, query: str, variables: Optional[Variables] = None
    ) -> ExecutionResultDict:
        """Be callable with optional variables."""
        ...


def dict_from_execution_result(result: ExecutionResult) -> ExecutionResultDict:
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
def graphql_query() -> QueryMethod:
    """Return a client query fn without logged in user."""

    def func(
        query: str, variables: Optional[Variables] = None
    ) -> ExecutionResultDict:
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
def graphql_query_user(
    user: AbstractBaseUser,
) -> QueryMethod:
    """Return a client query fn."""

    def func(
        query: str, variables: Optional[Variables] = None
    ) -> ExecutionResultDict:
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
def user_client(
    client: client.Client, user: AbstractBaseUser
) -> client.Client:
    """Return logged in client."""
    client.force_login(user)
    return client


@pytest.fixture
def superuser_client(
    client: client.Client, superuser: AbstractBaseUser
) -> client.Client:
    """Return logged in super user client."""
    client.force_login(superuser)
    return client


@pytest.fixture
def test_client() -> APIClient:
    """Return a client that we can use to test DRF views."""
    return APIClient()


@pytest.fixture
def rest_client() -> APIClient:
    """Return a logged-out client to test DRF views."""
    return APIClient()


@pytest.fixture
def rest_user_client(user: AbstractBaseUser) -> APIClient:
    """Return a logged in client that we can use to test DRF views."""
    client = APIClient()
    client.force_authenticate(user)
    return client


@pytest.fixture
def png_image() -> bytes:
    """Return a simple png file."""
    return base64.b64decode(
        "iVBORw0KGgoAAAANSUhEUgAAACAAAAAgAgAAAAAcoT2JAAAABGdBTUEAAYagMeiWX\
        wAAAB9JREFUeJxjYAhd9R+M8TCIUMIAU4aPATMJH2OQuQcAvUl/gYsJiakAAAAASUVORK5\
        CYII="
    )


@pytest.fixture
def uploaded_file(png_image: bytes) -> SimpleUploadedFile:
    """Return an UploadFile instance of the above png file."""
    return SimpleUploadedFile("test.png", png_image)
