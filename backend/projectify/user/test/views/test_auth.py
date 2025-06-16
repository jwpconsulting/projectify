# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2024 JWP Consulting GK
"""User auth view tests."""

from typing import Any

from django.test import Client
from django.urls import reverse

import pytest
from faker import Faker
from rest_framework.test import APIClient, RequestsClient

from projectify.settings.base import Base
from projectify.user.services.auth import user_sign_up
from projectify.user.services.internal import user_make_token
from pytest_types import DjangoAssertNumQueries

from ...models import User

pytestmark = pytest.mark.django_db


# Django view tests
class TestLogOutDjango:
    """Test log_out view."""

    @pytest.fixture
    def resource_url(self) -> str:
        """Return URL to this view."""
        return reverse("users-django:log-out")

    def test_log_out(
        self,
        client: Client,
        resource_url: str,
        django_assert_num_queries: DjangoAssertNumQueries,
        user: User,
        password: str,
    ) -> None:
        """Test logging out a user."""
        # First log in
        response = client.post(
            reverse("users-django:log-in"),
            {"email": user.email, "password": password},
            follow=True,
        )
        assert response.status_code == 200, response.content
        assert "user" in response.context, response.context
        assert response.context["user"].is_authenticated, response.content

        # Now log out
        with django_assert_num_queries(4):
            response = client.post(resource_url, follow=True)
        assert response.status_code == 200, response.content
        assert response.redirect_chain == [
            (reverse("storefront:landing"), 302)
        ]
        assert (
            response.context["user"].is_authenticated is False
        ), response.content


class TestSignUpDjango:
    """Test sign_up view."""

    @pytest.fixture
    def resource_url(self) -> str:
        """Return URL to this view."""
        return reverse("users-django:sign-up")

    def test_signing_up(
        self,
        client: Client,
        resource_url: str,
        django_assert_num_queries: DjangoAssertNumQueries,
        faker: Faker,
    ) -> None:
        """Test signing up a new user."""
        assert User.objects.count() == 0
        with django_assert_num_queries(9):
            response = client.post(
                resource_url,
                {
                    "email": "hello@localhost",
                    "password": faker.password(),
                    "tos_agreed": True,
                    "privacy_policy_agreed": True,
                },
                follow=True,
            )
        assert response.status_code == 200, response.content
        assert User.objects.count() == 1
        assert response.redirect_chain == [("/", 302)]

    def test_rate_limit(
        self,
        client: Client,
        resource_url: str,
        faker: Faker,
        settings: Base,
    ) -> None:
        """Test signing up a new user."""
        settings.RATELIMIT_ENABLE = True
        for i in range(4):
            response = client.post(
                resource_url,
                {
                    "email": faker.email(),
                    "password": faker.password(),
                    "tos_agreed": True,
                    "privacy_policy_agreed": True,
                },
            )
            assert response.status_code == 302  # Redirect status
            assert User.objects.count() == i + 1
        # The 5th request should be rate limited
        response = client.post(
            resource_url,
            {
                "email": faker.email(),
                "password": faker.password(),
                "tos_agreed": True,
                "privacy_policy_agreed": True,
            },
        )
        # The view creates no new user
        assert User.objects.count() == 4
        assert response.status_code == 429

    def test_signing_up_weak_pw(
        self,
        client: Client,
        resource_url: str,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Test signing up a new user with a weak password."""
        with django_assert_num_queries(1):
            response = client.post(
                resource_url,
                {
                    "email": "password@localhost",
                    "password": "password",
                    "tos_agreed": True,
                    "privacy_policy_agreed": True,
                },
            )
            assert response.status_code == 400

        assert b"The password is too similar to the Email" in response.content
        assert b"This password is too common" in response.content
        assert User.objects.count() == 0


class TestConfirmEmailDjango:
    """Test confirm_email Django view."""

    def test_confirm_email(
        self,
        client: Client,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Test confirming a new user's email address."""
        user = user_sign_up(
            email="hello@world.com",
            password="random_password",
            tos_agreed=True,
            privacy_policy_agreed=True,
        )
        token = user_make_token(user=user, kind="confirm_email_address")
        with django_assert_num_queries(6):
            response = client.get(
                reverse(
                    "users-django:confirm-email",
                    args=("hello@world.com", token),
                ),
                follow=True,
            )
        assert response.status_code == 200, response.content

        user.refresh_from_db()
        assert user.is_active

    def test_confirm_email_invalid_token(
        self,
        client: Client,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Test confirming with an invalid token."""
        user = user_sign_up(
            email="hello@world.com",
            password="random_password",
            tos_agreed=True,
            privacy_policy_agreed=True,
        )
        with django_assert_num_queries(1):
            response = client.get(
                reverse(
                    "users-django:confirm-email",
                    args=("hello@world.com", "invalid_token"),
                ),
                follow=True,
            )
        assert response.status_code == 200, response.content
        assert b"could not be confirmed" in response.content

        user.refresh_from_db()
        assert not user.is_active


class TestLogInDjango:
    """Test django log in view."""

    @pytest.fixture
    def resource_url(self) -> str:
        """Return URL to this view."""
        return reverse("users-django:log-in")

    def test_log_in(
        self,
        client: Client,
        resource_url: str,
        django_assert_num_queries: DjangoAssertNumQueries,
        user: User,
        password: str,
    ) -> None:
        """Test logging in a user."""
        # 13 + 3, 3 for the queries when redirecting
        with django_assert_num_queries(16):
            response = client.post(
                resource_url,
                {"email": user.email, "password": password},
                follow=True,
            )
        assert response.status_code == 200, response.content
        assert response.redirect_chain == [
            (reverse("dashboard:dashboard"), 302),
            (reverse("dashboard:workspaces:list"), 302),
        ]
        # Thx to
        # https://stackoverflow.com/questions/22457557/how-to-test-login-process/22458380#22458380
        assert "user" in response.context
        assert response.context["user"].is_authenticated, response.context

    def test_log_in_wrong_password(
        self,
        client: Client,
        resource_url: str,
        django_assert_num_queries: DjangoAssertNumQueries,
        user: User,
    ) -> None:
        """Test logging in with wrong password."""
        with django_assert_num_queries(2):
            response = client.post(
                resource_url,
                {"email": user.email, "password": "wrong_password"},
            )
        assert response.status_code == 400, response.content
        assert "user" in response.context
        assert response.context["user"].is_authenticated is False

    def test_log_in_with_next(
        self,
        client: Client,
        resource_url: str,
        user: User,
        password: str,
    ) -> None:
        """Test logging in with a next parameter."""
        dashboard_url = reverse("dashboard:dashboard")
        response = client.post(
            f"{resource_url}?next={dashboard_url}",
            {"email": user.email, "password": password},
            follow=True,
        )
        assert response.status_code == 200, response.content
        # There may be more than one element in this chain
        assert response.redirect_chain[0] == (dashboard_url, 302)
        assert response.context["user"].is_authenticated


class TestPasswordResetRequestDjango:
    """Test password reset request Django view."""

    @pytest.fixture
    def resource_url(self) -> str:
        """Return URL to this view."""
        return reverse("users-django:request-password-reset")

    def test_get_password_reset_request(
        self,
        client: Client,
        resource_url: str,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Test GETting the password reset request form."""
        with django_assert_num_queries(0):
            response = client.get(resource_url)
        assert response.status_code == 200, response.content
        assert b"Reset your password" in response.content

    def test_post_password_reset_request(
        self,
        client: Client,
        resource_url: str,
        django_assert_num_queries: DjangoAssertNumQueries,
        user: User,
    ) -> None:
        """Test POST request to password reset request page."""
        with django_assert_num_queries(1):
            response = client.post(
                resource_url,
                {"email": user.email},
                follow=True,
            )
            assert response.status_code == 200, response.content
        assert response.redirect_chain == [
            (reverse("users-django:requested-password-reset"), 302)
        ]

    def test_post_password_reset_request_invalid_email(
        self,
        client: Client,
        resource_url: str,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Test POST request with invalid email."""
        with django_assert_num_queries(0):
            response = client.post(
                resource_url,
                {"email": "invalid-email"},
            )
        assert response.status_code == 400, response.content

    def test_post_password_reset_request_nonexistent_email(
        self,
        client: Client,
        resource_url: str,
        django_assert_num_queries: DjangoAssertNumQueries,
        faker: Faker,
    ) -> None:
        """Test POST request with email that doesn't exist in the system."""
        nonexistent_email = faker.email()
        with django_assert_num_queries(1):
            response = client.post(
                resource_url,
                {"email": nonexistent_email},
            )
        assert response.status_code == 400, response.content


class TestPasswordResetRequestedDjango:
    """Test password reset requested Django view."""

    @pytest.fixture
    def resource_url(self) -> str:
        """Return URL to this view."""
        return reverse("users-django:requested-password-reset")

    def test_get_password_reset_requested(
        self,
        client: Client,
        resource_url: str,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Test GETting the password reset requested page."""
        with django_assert_num_queries(0):
            response = client.get(resource_url)
        assert response.status_code == 200, response.content
        assert b"Password reset requested" in response.content
        assert (
            b"You have requested for your password to be reset"
            in response.content
        )


# APIView tests
class TestLogOut:
    """Test logging out."""

    @pytest.fixture
    def log_in_url(self) -> str:
        """Return URL to log in."""
        return reverse("user:auth:log-in")

    @pytest.fixture
    def resource_url(self) -> str:
        """Return URL to this view."""
        return reverse("user:auth:log-out")

    def test_log_out_after_log_in(
        self,
        user: User,
        rest_client: APIClient,
        log_in_url: str,
        resource_url: str,
        django_assert_num_queries: DjangoAssertNumQueries,
        password: str,
    ) -> None:
        """Test as an authenticated user."""
        # Not using rest_user_client here since it's forced logged in
        response = rest_client.post(
            log_in_url,
            data={"email": user.email, "password": password},
        )
        assert response.status_code == 200, response.data
        with django_assert_num_queries(4):
            response = rest_client.post(resource_url)
            assert response.status_code == 200, response.data
        assert response.data == {"kind": "unauthenticated"}
        # Now that we are logged out, logging out another time is not allowed
        response = rest_client.post(resource_url)
        assert response.status_code == 403, response.data

    def test_log_out_without_csrf(
        self,
        user: User,
        log_in_url: str,
        resource_url: str,
        password: str,
        live_server: Any,
    ) -> None:
        """Ensure we can log't log out without a CSRF token."""
        client = RequestsClient()
        # We log in
        response = client.post(
            live_server.url + log_in_url,
            data={"email": user.email, "password": password},
        )
        assert response.status_code == 200, response.json()
        # Manually add cookies
        csrftoken = response.cookies["csrftoken"]
        headers = {
            "X-CSRFToken": csrftoken,
            "Cookie": f"sessionid={response.cookies['sessionid']};csrftoken={csrftoken}",
        }
        no_x_csrf_header = {"Cookie": headers["Cookie"]}
        # We prove that we are logged in
        response = client.get(
            live_server + reverse("user:users:read"), headers=headers
        )
        assert response.status_code == 200, response.json()
        assert response.json() == {
            "email": user.email,
            "kind": "authenticated",
            "preferred_name": user.preferred_name,
            "profile_picture": None,
        }
        # Perform dummy update
        response = client.put(
            live_server + reverse("user:users:update"), headers=headers
        )
        assert response.status_code == 200, response.json()

        response = client.put(
            live_server + reverse("user:users:update"),
            headers=no_x_csrf_header,
        )
        assert response.status_code == 403, response.json()
        # Log out won't work
        response = client.post(
            live_server + resource_url, headers=no_x_csrf_header
        )
        assert response.status_code == 403, response.json()
        # Now it works
        response = client.post(live_server + resource_url, headers=headers)
        assert response.status_code == 200, response.json()


# Now testing views that do not require to be logged in
class TestSignUp:
    """Test signing up."""

    @pytest.fixture
    def resource_url(self) -> str:
        """Return URL to this view."""
        return reverse("user:auth:sign-up")

    def test_signing_up(
        self,
        rest_client: APIClient,
        resource_url: str,
        django_assert_num_queries: DjangoAssertNumQueries,
        faker: Faker,
    ) -> None:
        """Test signing up a new user."""
        assert User.objects.count() == 0
        with django_assert_num_queries(9):
            response = rest_client.post(
                resource_url,
                # TODO of course, we will validate password strength here in
                # the future
                data={
                    "email": "hello@localhost",
                    "password": faker.password(),
                    "tos_agreed": True,
                    "privacy_policy_agreed": True,
                },
            )
            assert response.status_code == 204, response.data
        assert User.objects.count() == 1

    def test_rate_limit(
        self,
        rest_client: APIClient,
        resource_url: str,
        faker: Faker,
        settings: Base,
    ) -> None:
        """Test signing up a new user."""
        settings.RATELIMIT_ENABLE = True
        for _ in range(5):
            response = rest_client.post(
                resource_url,
                data={
                    "email": faker.email(),
                    "password": faker.password(),
                    "tos_agreed": True,
                    "privacy_policy_agreed": True,
                },
            )
            assert response.status_code == 204
        response = rest_client.post(
            resource_url,
            data={
                "email": faker.email(),
                "password": faker.password(),
                "tos_agreed": True,
                "privacy_policy_agreed": True,
            },
        )
        assert response.status_code == 429

    def test_signing_up_weak_pw(
        self,
        rest_client: APIClient,
        resource_url: str,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Test signing up a new user."""
        with django_assert_num_queries(1):
            response = rest_client.post(
                resource_url,
                data={
                    "email": "password@localhost",
                    "password": "password",
                    "tos_agreed": True,
                    "privacy_policy_agreed": True,
                },
            )
            assert response.status_code == 400, response.data
        assert response.data == {
            "status": "invalid",
            "code": 400,
            "details": {
                "password": "The password is too similar to the Email. "
                "This password is too common."
            },
            "general": None,
        }


class TestConfirmEmail:
    """Test confirming a newly registered user's email address."""

    @pytest.fixture
    def resource_url(self) -> str:
        """Return URL to this view."""
        return reverse("user:auth:confirm-email")

    def test_confirm_for_new_user(
        self,
        rest_client: APIClient,
        resource_url: str,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Test the thing that I want to test."""
        user = user_sign_up(
            email="hello@world.com",
            password="random_password",
            tos_agreed=True,
            privacy_policy_agreed=True,
        )
        token = user_make_token(user=user, kind="confirm_email_address")
        with django_assert_num_queries(6):
            response = rest_client.post(
                resource_url,
                data={"email": "hello@world.com", "token": token},
            )
        assert response.status_code == 204, response.data

        user.refresh_from_db()
        assert user.is_active


class TestLogIn:
    """Test logging in."""

    @pytest.fixture
    def resource_url(self) -> str:
        """Return URL to this view."""
        return reverse("user:auth:log-in")

    # TODO test rate limiting
    def test_authenticated_user(
        self,
        rest_client: APIClient,
        resource_url: str,
        user: User,
        django_assert_num_queries: DjangoAssertNumQueries,
        password: str,
    ) -> None:
        """Test as an authenticated user."""
        with django_assert_num_queries(13):
            response = rest_client.post(
                resource_url,
                data={"email": user.email, "password": password},
            )
            assert response.status_code == 200, response.data
        assert response.data == {
            "kind": "authenticated",
            "email": user.email,
            "profile_picture": None,
            "preferred_name": user.preferred_name,
        }


class TestPasswordResetRequest:
    """Test requesting a password reset."""

    @pytest.fixture
    def resource_url(self) -> str:
        """Return URL to this view."""
        return reverse("user:auth:request-password-reset")

    def test_request_password_reset(
        self,
        user: User,
        rest_client: APIClient,
        resource_url: str,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Test requesting a password reset for a user."""
        with django_assert_num_queries(1):
            response = rest_client.post(
                resource_url,
                data={"email": user.email},
            )
            assert response.status_code == 204, response.data


class TestPasswordResetConfirm:
    """Test confirming a password reset."""

    @pytest.fixture
    def request_url(self) -> str:
        """Return URL to request the reset."""
        return reverse("user:auth:request-password-reset")

    @pytest.fixture
    def resource_url(self) -> str:
        """Return URL to this view."""
        return reverse("user:auth:confirm-password-reset")

    def test_confirm_password_reset(
        self,
        user: User,
        rest_client: APIClient,
        request_url: str,
        resource_url: str,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Test confirming the password reset for a user."""
        response = rest_client.post(
            request_url,
            data={"email": user.email},
        )
        assert response.status_code == 204, response.data
        # We are somewhat cheating here since we don't check the email outbox
        token = user_make_token(user=user, kind="reset_password")
        with django_assert_num_queries(8):
            response = rest_client.post(
                resource_url,
                # TODO of course in the future we will validate password strength
                # here
                data={
                    "email": user.email,
                    "token": token,
                    "new_password": "evenmoresecurepassword123",
                },
            )
            assert response.status_code == 204, response.data
        user.refresh_from_db()
        assert user.check_password("evenmoresecurepassword123")


class TestPasswordPolicyRead:
    """Test password policy read."""

    @pytest.fixture
    def resource_url(self) -> str:
        """Return URL to this view."""
        return reverse("user:auth:password-policy")

    def test_get(
        self,
        rest_client: APIClient,
        resource_url: str,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Test GET."""
        with django_assert_num_queries(0):
            response = rest_client.get(resource_url)
        assert response.status_code == 200, response.data
        assert response.data == {
            "policies": [
                "Your password can’t be too similar to your other personal "
                "information.",
                "Your password must contain at least 8 characters.",
                "Your password can’t be a commonly used password.",
                "Your password can’t be entirely numeric.",
            ]
        }
