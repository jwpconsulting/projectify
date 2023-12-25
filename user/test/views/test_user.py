"""User view tests."""
from collections.abc import (
    Mapping,
)
from typing import (
    Any,
)

from django.core.files import (
    File,
)
from django.test import (
    Client,
)
from django.urls import (
    reverse,
)

import pytest
from rest_framework.status import HTTP_200_OK
from rest_framework.test import APIClient

from pytest_types import DjangoAssertNumQueries
from user.services.user import user_sign_up

from ...models import User

Headers = Mapping[str, Any]


# Create
# Read + Update
@pytest.mark.django_db
class TestUserReadUpdate:
    """Test UserReadUpdate view."""

    @pytest.fixture
    def resource_url(self) -> str:
        """Return URL to this view."""
        return reverse("user:users:read-update")

    def test_authenticated(
        self, user_client: Client, resource_url: str, user: User
    ) -> None:
        """Assert we can post to this view this while being logged in."""
        response = user_client.get(resource_url)
        assert response.status_code == 200, response.content

    def test_update(
        self,
        rest_user_client: APIClient,
        resource_url: str,
        django_assert_num_queries: DjangoAssertNumQueries,
        user: User,
    ) -> None:
        """Test updating."""
        with django_assert_num_queries(1):
            response = rest_user_client.put(
                resource_url,
                data={},
            )
            assert response.status_code == HTTP_200_OK, response.data
        user.refresh_from_db()
        assert user.full_name is None
        response = rest_user_client.put(
            resource_url,
            data={"full_name": "Locutus of Blorb"},
        )
        user.refresh_from_db()
        assert user.full_name == "Locutus of Blorb"


# Delete


# RPC
@pytest.mark.django_db
class TestProfilePictureUploadView:
    """Test ProfilePictureUploadView."""

    @pytest.fixture
    def resource_url(self) -> str:
        """Return URL to this view."""
        return reverse("user:users:upload-profile-picture")

    @pytest.fixture
    def headers(self, png_image: File) -> Headers:
        """Return headers."""
        return {
            "HTTP_CONTENT_DISPOSITION": "attachment; filename=test.png",
            "HTTP_CONTENT_LENGTH": len(png_image),
        }

    def test_unauthenticated(
        self,
        client: Client,
        resource_url: str,
        headers: Headers,
        uploaded_file: File,
    ) -> None:
        """Assert we can't view this while being logged out."""
        response = client.post(
            resource_url,
            {"file": uploaded_file},
            format="multipart",
            **headers,
        )

        assert response.status_code == 403, response.content

    def test_authenticated(
        self,
        user_client: Client,
        resource_url: str,
        headers: Headers,
        uploaded_file: File,
        user: User,
    ) -> None:
        """Assert we can post to this view this while being logged in."""
        response = user_client.post(
            resource_url,
            {"file": uploaded_file},
            format="multipart",
            **headers,
        )
        assert response.status_code == 204, response.content
        user.refresh_from_db()
        assert user.profile_picture is not None


# TODO these should be in user/test/views/test_auth.py
@pytest.mark.django_db
class TestLogOut:
    """Test logging out."""

    @pytest.fixture
    def log_in_url(self) -> str:
        """Return URL to log in."""
        return reverse("user:users:log-in")

    @pytest.fixture
    def resource_url(self) -> str:
        """Return URL to this view."""
        return reverse("user:users:log-out")

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
        assert response.status_code == 204, response.data
        with django_assert_num_queries(4):
            response = rest_client.post(resource_url)
            assert response.status_code == 204, response.data
        # Now that we are logged out, logging out another time is not allowed
        response = rest_client.post(resource_url)
        assert response.status_code == 403, response.data


# Now testing views that do not require to be logged in
@pytest.mark.django_db
class TestSignUp:
    """Test signing up."""

    @pytest.fixture
    def resource_url(self) -> str:
        """Return URL to this view."""
        return reverse("user:users:sign-up")

    def test_signing_up(
        self,
        rest_client: APIClient,
        resource_url: str,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Test signing up a new user."""
        assert User.objects.count() == 0
        with django_assert_num_queries(5):
            response = rest_client.post(
                resource_url,
                # TODO of course, we will validate password strength here in
                # the future
                data={
                    "email": "hello@localhost",
                    "password": "password",
                    "tos_agreed": True,
                    "privacy_policy_agreed": True,
                },
            )
            assert response.status_code == 204, response.data
        assert User.objects.count() == 1


@pytest.mark.django_db
class TestConfirmEmail:
    """Test confirming a newly registered user's email address."""

    @pytest.fixture
    def resource_url(self) -> str:
        """Return URL to this view."""
        return reverse("user:users:confirm-email")

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
        token = user.get_email_confirmation_token()
        with django_assert_num_queries(2):
            response = rest_client.post(
                resource_url,
                data={"email": "hello@world.com", "token": token},
            )
        assert response.status_code == 204, response.data

        user.refresh_from_db()
        assert user.is_active


@pytest.mark.django_db
class TestLogIn:
    """Test logging in."""

    @pytest.fixture
    def resource_url(self) -> str:
        """Return URL to this view."""
        return reverse("user:users:log-in")

    def test_authenticated_user(
        self,
        rest_client: APIClient,
        resource_url: str,
        user: User,
        django_assert_num_queries: DjangoAssertNumQueries,
        password: str,
    ) -> None:
        """Test as an authenticated user."""
        with django_assert_num_queries(9):
            response = rest_client.post(
                resource_url,
                data={"email": user.email, "password": password},
            )
            assert response.status_code == 204, response.data


@pytest.mark.django_db
class TestPasswordResetRequest:
    """Test requesting a password reset."""

    @pytest.fixture
    def resource_url(self) -> str:
        """Return URL to this view."""
        return reverse("user:users:request-password-reset")

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


@pytest.mark.django_db
class TestPasswordResetConfirm:
    """Test confirming a password reset."""

    @pytest.fixture
    def request_url(self) -> str:
        """Return URL to request the reset."""
        return reverse("user:users:request-password-reset")

    @pytest.fixture
    def resource_url(self) -> str:
        """Return URL to this view."""
        return reverse("user:users:confirm-password-reset")

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
        token = user.get_password_reset_token()
        with django_assert_num_queries(4):
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
