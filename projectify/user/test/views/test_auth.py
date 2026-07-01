# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2024 JWP Consulting GK
"""User auth view tests."""

from collections.abc import Generator
from unittest.mock import MagicMock, patch

from django.core.cache import cache
from django.test import Client
from django.urls import reverse

import pytest
from faker import Faker

from projectify.settings.base import Base
from pytest_types import DjangoAssertNumQueries

from ...models import User
from ...services.auth import user_sign_up
from ...services.internal import user_make_token

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
        data = {"email": user.email, "password": password}
        response = client.post(reverse("users:log-in"), data, follow=True)
        assert response.status_code == 200, response.content
        assert "user" in response.context, response.context
        assert response.context["user"].is_authenticated, response.content
        # Now log out
        # went up from 6 -> 7 because we show blog posts on the landing page
        with django_assert_num_queries(7):
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
        data = {
            "email": "hello@localhost",
            "password": faker.password(),
            "tos_agreed": True,
            "privacy_policy_agreed": True,
        }
        with django_assert_num_queries(11):
            response = client.post(resource_url, data, follow=True)
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
        data = {
            "email": "password@localhost",
            "password": "password",
            "tos_agreed": True,
            "privacy_policy_agreed": True,
        }
        with django_assert_num_queries(5):
            response = client.post(resource_url, data)
            assert response.status_code == 400
        assert b"The password is too similar to the Email" in response.content
        assert b"This password is too common" in response.content
        assert User.objects.count() == 0

    def test_rate_limit(
        self, client: Client, resource_url: str, faker: Faker, settings: Base
    ) -> None:
        """Test signing up a new user."""
        settings.RATELIMIT_ENABLE = True
        for i in range(4):
            data = {
                "email": faker.email(),
                "password": faker.password(),
                "tos_agreed": True,
                "privacy_policy_agreed": True,
            }
            response = client.post(resource_url, data)
            assert response.status_code == 302  # Redirect status
            assert User.objects.count() == i + 1
        # The 5th request should be rate limited
        data = {
            "email": faker.email(),
            "password": faker.password(),
            "tos_agreed": True,
            "privacy_policy_agreed": True,
        }
        response = client.post(resource_url, data)
        # The view creates no new user
        # XXX flaky
        assert User.objects.count() == 4, User.objects.all()
        assert response.status_code == 429

    def test_rate_limit_per_ip_regardless_of_success(
        self, client: Client, resource_url: str, faker: Faker, settings: Base
    ) -> None:
        """Test rate limiting by IP address (10/h regardless of success)."""
        cache.clear()
        settings.RATELIMIT_ENABLE = True

        # Make 10 requests with invalid data (should all fail but count towards limit)
        data = {
            "email": "invalid-email",  # Invalid email format
            "password": faker.password(),
            "tos_agreed": True,
            "privacy_policy_agreed": True,
        }
        for i in range(10):
            response = client.post(resource_url, data)
            assert response.status_code == 400, f"Attempt {i}"

        # The 11th request should be rate limited
        data = {
            "email": faker.email(),
            "password": faker.password(),
            "tos_agreed": True,
            "privacy_policy_agreed": True,
        }
        response = client.post(resource_url, data)
        assert response.status_code == 429
        assert User.objects.count() == 0


class TestSocialAccountSignupView:
    """Test socialaccount_signup view."""

    @pytest.fixture(autouse=True)
    def mock_get_adapter(self) -> Generator[MagicMock, None, None]:
        """Mock get_adapter for social account tests."""
        mock_adapter = MagicMock()
        mock_adapter.get_signup_form_initial_data.return_value = {
            "email": "social@example.com"
        }
        with patch("projectify.user.forms.get_adapter") as mock_get_adapter:
            mock_get_adapter.return_value = mock_adapter
            yield mock_get_adapter

    @pytest.fixture(autouse=True)
    def mock_sociallogin_retrieval(self) -> Generator[MagicMock, None, None]:
        """Mock the retrieval of sociallogin from session."""
        mock_sociallogin = MagicMock(name="mock_sociallogin")
        mock_sociallogin.user = User()
        mock_sociallogin.get_redirect_url.return_value = "/"

        mock_account = MagicMock(name="mock_account")
        mock_account.provider = "allauth.socialaccounts.providers.github"
        mock_account.uid = "1"
        mock_sociallogin.account = mock_account
        mock_sociallogin.is_existing = False
        with patch(
            "allauth.socialaccount.views.flows.signup.get_pending_signup"
        ) as mock_get_pending:
            mock_get_pending.return_value = mock_sociallogin
            yield mock_sociallogin

    def test_cannot_overwrite_email(self, client: Client) -> None:
        """Test that user cannot overwrite email from social login."""
        data = {
            "email": "different@example.com",
            "tos_agreed": True,
            "privacy_policy_agreed": True,
        }
        response = client.post(reverse("socialaccount_signup"), data)
        assert response.status_code == 200
        assert b"email" in response.content
        assert User.objects.count() == 0

    def test_user_created_with_correct_email(self, client: Client) -> None:
        """Test that user is created when correct email is provided."""
        assert User.objects.count() == 0
        data = {
            "email": "social@example.com",
            "tos_agreed": True,
            "privacy_policy_agreed": True,
        }
        response = client.post(reverse("socialaccount_signup"), data)
        assert response.status_code == 302
        assert User.objects.count() == 1
        user = User.objects.get(email="social@example.com")
        assert user.email == "social@example.com"


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
        self, client: Client, django_assert_num_queries: DjangoAssertNumQueries
    ) -> None:
        """Test confirming a new user's email address."""
        user = user_sign_up(
            email="hello@world.com",
            password="random_password",
            tos_agreed=True,
            privacy_policy_agreed=True,
        )
        token = user_make_token(user=user, kind="confirm_email_address")
        url = reverse("users:confirm-email", args=("hello@world.com", token))
        with django_assert_num_queries(8):
            response = client.get(url, follow=True)
        assert response.status_code == 200, response.content

        user.refresh_from_db()
        assert user.is_active

    def test_confirm_email_invalid_token(
        self, client: Client, django_assert_num_queries: DjangoAssertNumQueries
    ) -> None:
        """Test confirming with an invalid token."""
        user = user_sign_up(
            email="hello@world.com",
            password="random_password",
            tos_agreed=True,
            privacy_policy_agreed=True,
        )
        url = reverse("users:confirm-email", args=("hello@world.com", "inv"))
        with django_assert_num_queries(4):
            response = client.get(url, follow=True)
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
        data = {"email": user.email, "password": password}
        with django_assert_num_queries(15):
            response = client.post(resource_url, data)
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
        data = {"email": user.email, "password": "wrong_password"}
        with django_assert_num_queries(6):
            response = client.post(resource_url, data)
        assert response.status_code == 400, response.content
        assert "user" in response.context
        assert response.context["user"].is_authenticated is False

    def test_log_in_with_next(
        self, client: Client, resource_url: str, user: User, password: str
    ) -> None:
        """Test logging in with a next parameter."""
        dashboard_url = reverse("dashboard:dashboard")
        url = f"{resource_url}?next={dashboard_url}"
        data = {"email": user.email, "password": password}
        response = client.post(url, data, follow=True)
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
        data = {"email": user.email}
        with django_assert_num_queries(3):
            response = client.post(resource_url, data, follow=True)
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
        data = {"email": "invalid-email"}
        with django_assert_num_queries(0):
            response = client.post(resource_url, data)
        assert response.status_code == 400, response.content

    def test_post_password_reset_request_nonexistent_email(
        self,
        client: Client,
        resource_url: str,
        django_assert_num_queries: DjangoAssertNumQueries,
        faker: Faker,
    ) -> None:
        """Test POST request with email that doesn't exist in the system."""
        data = {"email": faker.email()}
        with django_assert_num_queries(4):
            response = client.post(resource_url, data)
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
        # Projectify requires users to confirm their email first before being
        # able to request password resets
        for u in [*first_users, last_user]:
            u.is_active = True
            u.save()

        for i, user in enumerate(first_users):
            response = client.post(resource_url, {"email": user.email})
            assert (
                response.status_code == 302
            ), f"Attempt {i}, {response.content.decode()}"

        response = client.post(resource_url, {"email": last_user.email})
        assert response.status_code == 429

    def test_post_password_reset_request_inactive_user(
        self, client: Client, resource_url: str, inactive_user: User
    ) -> None:
        """Test POST request with an inactive (unconfirmed) user's email."""
        response = client.post(resource_url, {"email": inactive_user.email})
        assert response.status_code == 400, response.content
        assert b"activate this account first" in response.content


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
        new_pw = "evenmoresecurepassword123"
        data = {"new_password": new_pw, "new_password_confirm": new_pw}
        url = reverse("users:confirm-password-reset", args=(user.email, token))
        with django_assert_num_queries(8):
            response = client.post(url, data)
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
        url = reverse("users:confirm-password-reset", args=(user.email, token))
        with django_assert_num_queries(0):
            response = client.get(url)
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
        url = reverse("users:confirm-password-reset", args=(user.email, token))
        data = {"new_password": "123", "new_password_confirm": "456"}
        with django_assert_num_queries(3):
            response = client.post(url, data)
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
        url = reverse("users:confirm-password-reset", args=(user.email, "inv"))
        new_pw = "evenmoresecurepassword123"
        data = {"new_password": new_pw, "new_password_confirm": new_pw}
        with django_assert_num_queries(4):
            response = client.post(url, data)
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
        wrong_mail = faker.email()
        url = reverse("users:confirm-password-reset", args=(wrong_mail, token))
        new_pw = "evenmoresecurepassword123"
        data = {"new_password": new_pw, "new_password_confirm": new_pw}
        with django_assert_num_queries(4):
            response = client.post(url, data)
            assert response.status_code == 400, response.content
        assert b"email is not recognized" in response.content
        user.refresh_from_db()
        assert not user.check_password("evenmoresecurepassword123")

    def test_confirm_password_reset_weak_password(
        self,
        client: Client,
        django_assert_num_queries: DjangoAssertNumQueries,
        user: User,
        password: str,
    ) -> None:
        """Test confirming with a weak password."""
        token = user_make_token(user=user, kind="reset_password")
        url = reverse("users:confirm-password-reset", args=(user.email, token))
        data = {"new_password": "asd123", "new_password_confirm": "asd123"}
        with django_assert_num_queries(4):
            response = client.post(url, data)
            assert response.status_code == 400, response.content
        assert b"This password is too short" in response.content
        assert b"This password is too common" in response.content
        user.refresh_from_db()
        assert user.check_password(password)
