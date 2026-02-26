# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2024 JWP Consulting GK
"""User auth view tests."""

from django.core.cache import cache
from django.test import Client
from django.urls import reverse

import pytest
from faker import Faker

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
        return reverse("users:log-out")

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
            reverse("users:log-in"),
            {"email": user.email, "password": password},
            follow=True,
        )
        assert response.status_code == 200, response.content
        assert "user" in response.context, response.context
        assert response.context["user"].is_authenticated, response.content

        # Now log out
        with django_assert_num_queries(6):
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
        return reverse("users:sign-up")

    def test_signing_up(
        self,
        client: Client,
        resource_url: str,
        django_assert_num_queries: DjangoAssertNumQueries,
        faker: Faker,
    ) -> None:
        """Test signing up a new user."""
        assert User.objects.count() == 0
        with django_assert_num_queries(11):
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
        assert response.redirect_chain == [
            (reverse("users:sent-email-confirmation-link"), 302)
        ]

    def test_signing_up_weak_pw(
        self,
        client: Client,
        resource_url: str,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Test signing up a new user with a weak password."""
        with django_assert_num_queries(4):
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

    def test_rate_limit_per_ip_regardless_of_success(
        self,
        client: Client,
        resource_url: str,
        faker: Faker,
        settings: Base,
    ) -> None:
        """Test rate limiting by IP address (10/h regardless of success)."""
        cache.clear()
        settings.RATELIMIT_ENABLE = True

        # Make 10 requests with invalid data (should all fail but count towards limit)
        for i in range(10):
            response = client.post(
                resource_url,
                {
                    "email": "invalid-email",  # Invalid email format
                    "password": faker.password(),
                    "tos_agreed": True,
                    "privacy_policy_agreed": True,
                },
            )
            assert response.status_code == 400, f"Attempt {i}"

        # The 11th request should be rate limited
        response = client.post(
            resource_url,
            {
                "email": faker.email(),
                "password": faker.password(),
                "tos_agreed": True,
                "privacy_policy_agreed": True,
            },
        )
        assert response.status_code == 429
        assert User.objects.count() == 0


class TestEmailConfirmationLinkSent:
    """Test sign up confirmation view."""

    @pytest.fixture
    def resource_url(self) -> str:
        """Return URL to this view."""
        return reverse("users:sent-email-confirmation-link")

    def test_get_email_confirmation_link_sent(
        self,
        client: Client,
        resource_url: str,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Test GETting the email confirmation link sent page."""
        with django_assert_num_queries(0):
            response = client.get(resource_url)
        assert response.status_code == 200, response.content
        assert b"Email confirmation link sent" in response.content


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
        with django_assert_num_queries(8):
            response = client.get(
                reverse(
                    "users:confirm-email",
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
        with django_assert_num_queries(4):
            response = client.get(
                reverse(
                    "users:confirm-email",
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
        return reverse("users:log-in")

    def test_log_in(
        self,
        client: Client,
        resource_url: str,
        django_assert_num_queries: DjangoAssertNumQueries,
        user: User,
        password: str,
    ) -> None:
        """Test logging in a user."""
        with django_assert_num_queries(15):
            response = client.post(
                resource_url,
                {"email": user.email, "password": password},
            )
        assert response.status_code == 302, response.content
        assert "sessionid" in response.cookies

    def test_log_in_wrong_password(
        self,
        client: Client,
        resource_url: str,
        django_assert_num_queries: DjangoAssertNumQueries,
        user: User,
    ) -> None:
        """Test logging in with wrong password."""
        with django_assert_num_queries(5):
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

    def test_log_in_rate_limit_by_email(
        self, client: Client, resource_url: str, user: User, settings: Base
    ) -> None:
        """Test rate limiting by failed log in for email address (5/h)."""
        cache.clear()
        settings.RATELIMIT_ENABLE = True

        data = {"email": user.email, "password": "wrong_password"}
        i = 0
        for i in range(5):
            # Use a different IP to bypass the IP rate limit
            response = client.post(
                resource_url, data, REMOTE_ADDR=f"127.0.0.{i}"
            )
            assert response.status_code == 400, f"Attempt {i}"

        response = client.post(resource_url, data, REMOTE_ADDR=f"127.0.0.{i}")
        assert response.status_code == 429

    def test_log_in_rate_limit_by_ip(
        self, client: Client, resource_url: str, settings: Base, faker: Faker
    ) -> None:
        """Test rate limiting by IP address."""
        cache.clear()
        settings.RATELIMIT_ENABLE = True

        has_429 = False
        # I like deterministic tests. django-ratelimit does not work with
        # sliding windows, but fixed windows. see
        # https://github.com/jsocol/django-ratelimit/issues/64
        # Rate limit is
        # @ratelimit(key="ip", rate="5/m", method=UNSAFE)
        for email in [faker.email() for _ in range(11)]:
            data = {"email": email, "password": "w"}
            response = client.post(resource_url, data=data)
            if response.status_code == 429:
                has_429 = True
                break
        else:
            assert False, "Rate limit never hit"

        assert has_429


class TestPasswordResetRequestDjango:
    """Test password reset request Django view."""

    @pytest.fixture
    def resource_url(self) -> str:
        """Return URL to this view."""
        return reverse("users:request-password-reset")

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
        with django_assert_num_queries(3):
            response = client.post(
                resource_url,
                {"email": user.email},
                follow=True,
            )
            assert response.status_code == 200, response.content
        assert response.redirect_chain == [
            (reverse("users:requested-password-reset"), 302)
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
        with django_assert_num_queries(4):
            response = client.post(
                resource_url,
                {"email": nonexistent_email},
            )
        assert response.status_code == 400, response.content

    def test_password_reset_request_rate_limit_by_email(
        self, client: Client, resource_url: str, user: User, settings: Base
    ) -> None:
        """Test rate limiting by email address (5/h)."""
        cache.clear()
        settings.RATELIMIT_ENABLE = True

        data = {"email": user.email}
        i = 0
        for i in range(5):
            # Use a different IP to bypass the IP rate limit
            response = client.post(
                resource_url, data, REMOTE_ADDR=f"127.0.0.{i}"
            )
            assert response.status_code == 302, f"Attempt {i}"

        response = client.post(resource_url, data, REMOTE_ADDR=f"127.0.0.{i}")
        assert response.status_code == 429

    def test_password_reset_request_rate_limit_by_ip(
        self, client: Client, resource_url: str, settings: Base, faker: Faker
    ) -> None:
        """Test rate limiting by IP address (5/h)."""
        cache.clear()
        settings.RATELIMIT_ENABLE = True

        # Create 6 users for testing
        *first_users, last_user = [
            user_sign_up(
                email=faker.email(),
                password=faker.password(),
                tos_agreed=True,
                privacy_policy_agreed=True,
            )
            for _ in range(6)
        ]

        for i, user in enumerate(first_users):
            response = client.post(
                resource_url,
                {"email": user.email},
            )
            assert response.status_code == 302, f"Attempt {i}"

        response = client.post(
            resource_url,
            {"email": last_user.email},
        )
        assert response.status_code == 429


class TestPasswordResetRequestedDjango:
    """Test password reset requested Django view."""

    @pytest.fixture
    def resource_url(self) -> str:
        """Return URL to this view."""
        return reverse("users:requested-password-reset")

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


class TestPasswordResetConfirmDjango:
    """Test password_reset_confirm view."""

    def test_confirm_password_reset(
        self,
        client: Client,
        django_assert_num_queries: DjangoAssertNumQueries,
        user: User,
    ) -> None:
        """Test confirming the password reset for a user."""
        token = user_make_token(user=user, kind="reset_password")
        with django_assert_num_queries(8):
            response = client.post(
                reverse(
                    "users:confirm-password-reset",
                    args=(user.email, token),
                ),
                {
                    "new_password": "evenmoresecurepassword123",
                    "new_password_confirm": "evenmoresecurepassword123",
                },
            )
            assert response.status_code == 302, response.content

        user.refresh_from_db()
        assert user.check_password("evenmoresecurepassword123")

    def test_confirm_password_reset_get(
        self,
        client: Client,
        django_assert_num_queries: DjangoAssertNumQueries,
        user: User,
    ) -> None:
        """Test GET request to password reset confirm page."""
        token = user_make_token(user=user, kind="reset_password")

        with django_assert_num_queries(0):
            response = client.get(
                reverse(
                    "users:confirm-password-reset",
                    args=(user.email, token),
                ),
            )
            assert response.status_code == 200, response.content

        assert b"Reset your password" in response.content

    def test_confirm_password_reset_passwords_dont_match(
        self,
        client: Client,
        django_assert_num_queries: DjangoAssertNumQueries,
        user: User,
    ) -> None:
        """Test confirming with mismatched passwords."""
        token = user_make_token(user=user, kind="reset_password")

        with django_assert_num_queries(3):
            response = client.post(
                reverse(
                    "users:confirm-password-reset",
                    args=(user.email, token),
                ),
                {
                    "new_password": "password123",
                    "new_password_confirm": "differentpassword123",
                },
            )
            assert response.status_code == 400, response.content

        assert b"New passwords must match" in response.content

        user.refresh_from_db()
        assert not user.check_password("password123")
        assert not user.check_password("differentpassword123")

    def test_confirm_password_reset_invalid_token(
        self,
        client: Client,
        django_assert_num_queries: DjangoAssertNumQueries,
        user: User,
    ) -> None:
        """Test confirming with an invalid token."""
        with django_assert_num_queries(4):
            response = client.post(
                reverse(
                    "users:confirm-password-reset",
                    args=(user.email, "invalid_token"),
                ),
                {
                    "new_password": "evenmoresecurepassword123",
                    "new_password_confirm": "evenmoresecurepassword123",
                },
            )
            assert response.status_code == 400, response.content

        assert b"This token is invalid" in response.content

        user.refresh_from_db()
        assert not user.check_password("evenmoresecurepassword123")

    def test_confirm_password_reset_wrong_email(
        self,
        client: Client,
        django_assert_num_queries: DjangoAssertNumQueries,
        user: User,
        faker: Faker,
    ) -> None:
        """Test confirming with the wrong email address."""
        token = user_make_token(user=user, kind="reset_password")
        wrong_email = faker.email()

        with django_assert_num_queries(4):
            response = client.post(
                reverse(
                    "users:confirm-password-reset",
                    args=(wrong_email, token),
                ),
                {
                    "new_password": "evenmoresecurepassword123",
                    "new_password_confirm": "evenmoresecurepassword123",
                },
            )
            assert response.status_code == 400, response.content
        assert b"email is not recognized" in response.content

        user.refresh_from_db()
        assert not user.check_password("evenmoresecurepassword123")
