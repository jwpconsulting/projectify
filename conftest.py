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
from faker import Faker
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
from user.services.user import user_create, user_create_superuser
from user.services.user_invite import user_invite_create, user_invite_redeem


@pytest.fixture
def password(faker: Faker) -> str:
    """Set default password."""
    pw: str = faker.password(length=20)
    return pw


@pytest.fixture
def user(faker: Faker, password: str) -> user_models.User:
    """Return a db user."""
    user = user_create(email=faker.email(), password=password)
    user.is_active = True
    user.full_name = faker.name()
    user.save()
    return user


@pytest.fixture
def superuser(faker: Faker) -> user_models.User:
    """Return a db super user."""
    return user_create_superuser(email=faker.email())


@pytest.fixture
def other_user(faker: Faker) -> user_models.User:
    """Return another db user."""
    return user_create(email=faker.email())


@pytest.fixture
def unrelated_user(faker: Faker) -> user_models.User:
    """Return unrelated user normally not in the same workspace."""
    return user_create(email=faker.email())


@pytest.fixture
def meddling_user(faker: Faker, password: str) -> user_models.User:
    """Create a canary user to check permissions."""
    user = user_create(email=faker.email(), password=password)
    user.is_active = True
    user.full_name = faker.name()
    user.save()
    return user


@pytest.fixture
def inactive_user(faker: Faker, password: str) -> user_models.User:
    """Return an inactive db user."""
    return user_create(email=faker.email(), password=password)


@pytest.fixture
def user_invite(faker: Faker) -> user_models.UserInvite:
    """Return a user invite."""
    user_invite = user_invite_create(email=faker.email())
    if user_invite is None:
        raise ValueError("Expected user_invite")
    return user_invite


@pytest.fixture
def redeemed_user_invite(faker: Faker) -> user_models.UserInvite:
    """Return a redeemed user invite."""
    email = faker.email()
    user_invite = user_invite_create(email=email)
    if user_invite is None:
        raise AssertionError("Expected user_invite")
    user = user_create(email=email)
    user_invite_redeem(user=user, user_invite=user_invite)
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
def rest_meddling_client(meddling_user: AbstractBaseUser) -> APIClient:
    """Return a test client to check third party logged in access."""
    client = APIClient()
    client.force_authenticate(meddling_user)
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
