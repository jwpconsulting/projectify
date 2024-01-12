# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Copyright (C) 2023 JWP Consulting GK
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
"""Test user services."""
from django.contrib.auth.models import AnonymousUser
from django.contrib.sessions.middleware import SessionMiddleware
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.test import RequestFactory

import pytest
from faker import Faker
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from user.models import User
from user.services.user import (
    user_confirm_email,
    user_confirm_password_reset,
    user_create,
    user_create_superuser,
    user_log_in,
    user_log_out,
    user_request_password_reset,
    user_sign_up,
    user_update,
)

pytestmark = pytest.mark.django_db


def test_user_create() -> None:
    """Test creating a normal user."""
    u = user_create("hello@example")
    assert u.is_active is False


def test_user_create_superuser() -> None:
    """Test creating a superuser. A superuser should be active."""
    u = user_create_superuser("hello@example")
    assert u.is_active is True


def test_user_update(user: User, faker: Faker) -> None:
    """Test updating a user."""
    new_name = faker.name()
    user_update(who=user, user=user, full_name=new_name)
    user.refresh_from_db()
    assert user.full_name == new_name


def test_user_sign_up_no_agree(faker: Faker) -> None:
    """Test signing up a new user."""
    assert User.objects.count() == 0
    with pytest.raises(serializers.ValidationError):
        user_sign_up(
            email=faker.email(),
            password=faker.password(),
            tos_agreed=False,
            privacy_policy_agreed=False,
        )
    with pytest.raises(serializers.ValidationError) as error:
        user_sign_up(
            email=faker.email(),
            password=faker.password(),
            tos_agreed=False,
            privacy_policy_agreed=True,
        )
    assert error.match("terms of service")
    with pytest.raises(serializers.ValidationError) as error:
        user_sign_up(
            email=faker.email(),
            password=faker.password(),
            tos_agreed=True,
            privacy_policy_agreed=False,
        )
    assert error.match("privacy policy")
    assert User.objects.count() == 0


def test_user_sign_up(faker: Faker) -> None:
    """Test signing up a new user."""
    assert User.objects.count() == 0
    user_sign_up(
        email=faker.email(),
        password=faker.password(),
        tos_agreed=True,
        privacy_policy_agreed=True,
    )
    user = User.objects.get()
    assert user.privacy_policy_agreed is not None
    assert user.tos_agreed is not None


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


def test_user_log_in(
    user: User,
    password: str,
    session_request: HttpRequest,
) -> None:
    """Test logging in."""
    assert "_auth_user_id" not in session_request.session.keys()
    user_log_in(email=user.email, password=password, request=session_request)
    assert "_auth_user_id" in session_request.session.keys()


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
def test_user_log_out(
    session_request: HttpRequest, user: User, password: str
) -> None:
    """Test logging a user out."""
    # First we log in
    user_log_in(email=user.email, password=password, request=session_request)
    assert "_auth_user_id" in session_request.session.keys()
    user_log_out(request=session_request)
    assert "_auth_user_id" not in session_request.session.keys()


def test_user_log_out_not_logged_in(
    session_request: HttpRequest,
) -> None:
    """Test logging when not logged in."""
    assert "_auth_user_id" not in session_request.session.keys()
    with pytest.raises(ValidationError) as error:
        user_log_out(request=session_request)
    assert "no logged in user" in error.exconly()
    assert "_auth_user_id" not in session_request.session.keys()


def test_request_password_reset(
    user: User, faker: Faker, mailoutbox: list[object]
) -> None:
    """Test pw reset requests."""
    assert len(mailoutbox) == 0
    user_request_password_reset(email=user.email)
    assert len(mailoutbox) == 1
    with pytest.raises(ValidationError) as error:
        user_request_password_reset(email=faker.email())
    assert error.match("No user could be found")
    assert len(mailoutbox) == 1


def test_confirm_password_reset(
    user: User, password: str, faker: Faker
) -> None:
    """Test password reset confirmation."""
    new_password = faker.password()

    # First with right email, wrong token
    with pytest.raises(ValidationError) as error:
        user_confirm_password_reset(
            email=user.email,
            new_password=new_password,
            token="wrong token",
        )
    assert error.match("token is invalid")
    user.refresh_from_db()
    assert user.check_password(password)
    assert not user.check_password(new_password)

    # Then with right token, wrong email
    token = user.get_password_reset_token()
    with pytest.raises(ValidationError) as error:
        user_confirm_password_reset(
            email=faker.email(),
            new_password=new_password,
            token=token,
        )
    assert error.match("email is not recognized")
    user.refresh_from_db()
    assert not user.check_password(new_password)

    # Then with right token, right email
    user_confirm_password_reset(
        email=user.email,
        new_password=new_password,
        token=token,
    )
    user.refresh_from_db()
    assert user.check_password(new_password)

    # Then reuse old token, right email
    new_new_password = faker.password()
    with pytest.raises(ValidationError) as error:
        user_confirm_password_reset(
            email=user.email,
            new_password=new_new_password,
            token=token,
        )
    assert error.match("token is invalid")
    user.refresh_from_db()
    assert user.check_password(new_password)
    assert not user.check_password(new_new_password)
