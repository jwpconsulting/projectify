"""Test user services."""
from django.contrib.auth.models import AnonymousUser
from django.contrib.sessions.middleware import SessionMiddleware
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.test import RequestFactory

import pytest
from faker import Faker
from rest_framework.exceptions import ValidationError

from user.models import User
from user.services.user import (
    user_confirm_email,
    user_create,
    user_create_superuser,
    user_log_in,
    user_log_out,
    user_sign_up,
)


@pytest.mark.django_db
def test_user_create() -> None:
    """Test creating a normal user."""
    u = user_create("hello@example")
    assert u.is_active is False


@pytest.mark.django_db
def test_user_create_superuser() -> None:
    """Test creating a superuser. A superuser should be active."""
    u = user_create_superuser("hello@example")
    assert u.is_active is True


@pytest.mark.django_db
def test_user_sign_up(faker: Faker) -> None:
    """Test signing up a new user."""
    assert User.objects.count() == 0
    user_sign_up(email=faker.email(), password=faker.password())
    assert User.objects.count() == 1


@pytest.mark.django_db
def test_user_confirm_email(user: User, inactive_user: User) -> None:
    """Test activating an active and inactive user."""
    assert user.is_active
    user_confirm_email(
        email=user.email,
        token=user.get_email_confirmation_token(),
    )
    user.refresh_from_db()
    assert user.is_active

    assert not inactive_user.is_active
    user_confirm_email(
        email=inactive_user.email,
        token=inactive_user.get_email_confirmation_token(),
    )
    inactive_user.refresh_from_db()
    assert inactive_user.is_active


@pytest.fixture
def session_middleware() -> SessionMiddleware:
    """Create a session middlware instance."""
    return SessionMiddleware(lambda _x: HttpResponse())


@pytest.fixture
def session_request(
    session_middleware: SessionMiddleware, rf: RequestFactory
) -> HttpRequest:
    """Return a request containing a session needed to test auth."""
    request = rf.get("/")
    session_middleware.process_request(request)
    request.session.save()
    request.user = AnonymousUser()
    return request


@pytest.mark.django_db
def test_user_log_in(
    user: User,
    password: str,
    session_request: HttpRequest,
) -> None:
    """Test logging in."""
    assert "_auth_user_id" not in session_request.session.keys()
    user_log_in(email=user.email, password=password, request=session_request)
    assert "_auth_user_id" in session_request.session.keys()


@pytest.mark.django_db
def test_user_log_in_wrong_password(
    user: User,
    session_request: HttpRequest,
) -> None:
    """Test logging in with wrong password."""
    # First with active user
    assert "_auth_user_id" not in session_request.session.keys()
    with pytest.raises(ValidationError) as error:
        user_log_in(
            email=user.email,
            password="wrongpassword",
            request=session_request,
        )
    assert "password is incorrect" in error.exconly()
    assert "_auth_user_id" not in session_request.session.keys()


@pytest.mark.django_db
def test_user_log_in_inactive(
    inactive_user: User,
    password: str,
    session_request: HttpRequest,
) -> None:
    """Test logging in as an inactive user."""
    # First with active user
    assert "_auth_user_id" not in session_request.session.keys()
    with pytest.raises(ValidationError) as error:
        user_log_in(
            email=inactive_user.email,
            password=password,
            request=session_request,
        )
    assert "not been confirmed" in error.exconly()
    assert "_auth_user_id" not in session_request.session.keys()


# - user_log_out
@pytest.mark.django_db
def test_user_log_out(
    session_request: HttpRequest, user: User, password: str
) -> None:
    """Test logging a user out."""
    # First we log in
    user_log_in(email=user.email, password=password, request=session_request)
    assert "_auth_user_id" in session_request.session.keys()
    user_log_out(request=session_request)
    assert "_auth_user_id" not in session_request.session.keys()


@pytest.mark.django_db
def test_user_log_out_not_logged_in(
    session_request: HttpRequest,
) -> None:
    """Test logging when not logged in."""
    assert "_auth_user_id" not in session_request.session.keys()
    with pytest.raises(ValidationError) as error:
        user_log_out(request=session_request)
    assert "no logged in user" in error.exconly()
    assert "_auth_user_id" not in session_request.session.keys()


# - user_request_password_reset
# - user_confirm_password_reset
