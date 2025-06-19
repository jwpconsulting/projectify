# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2022, 2023 JWP Consulting GK
"""User view tests."""

from collections.abc import Mapping
from typing import Any

from django.core.files import File
from django.test.client import Client
from django.urls import reverse

import pytest
from faker import Faker
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_403_FORBIDDEN,
)
from rest_framework.test import APIClient

from projectify.lib.settings import Base
from projectify.user.services.internal import user_make_token
from pytest_types import DjangoAssertNumQueries

from ...models import User

pytestmark = pytest.mark.django_db

Headers = Mapping[str, Any]


# Django view tests


class TestUserProfile:
    """Test django user_profile view."""


class TestPasswordChangeDjango:
    """Test django password_change view."""

    @pytest.fixture
    def resource_url(self) -> str:
        """Return URL to this view."""
        return reverse("users-django:change-password")

    def test_with_correct_password(
        self,
        user: User,
        password: str,
        user_client: Client,
        resource_url: str,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Test changing password with a good password."""
        with django_assert_num_queries(20):
            response = user_client.post(
                resource_url,
                {
                    "current_password": password,
                    "new_password": "hello-world123",
                    "new_password_confirm": "hello-world123",
                },
                follow=True,
            )
            assert response.status_code == 200, response.content
        assert response.wsgi_request.user.is_authenticated
        user.refresh_from_db()
        assert user.check_password("hello-world123")

    def test_with_incorrect_password(
        self,
        user: User,
        user_client: Client,
        resource_url: str,
    ) -> None:
        """Test changing password with an incorrect current password."""
        response = user_client.post(
            resource_url,
            {
                "current_password": "wrong-password",
                "new_password": "new-password123",
                "new_password_confirm": "new-password123",
            },
        )
        # Should return to the form with an error
        assert response.status_code == 400, response.content
        # Check that the form has an error
        assert "current_password" in response.context["form"].errors
        # Verify password was not changed
        user.refresh_from_db()
        assert not user.check_password("new-password123")

    def test_with_weak_new_password(
        self,
        user: User,
        password: str,
        user_client: Client,
        resource_url: str,
    ) -> None:
        """Test changing password with a weak new password."""
        response = user_client.post(
            resource_url,
            {
                "current_password": password,
                "new_password": "123456",
                "new_password_confirm": "123456",
            },
        )
        # Should return to the form with an error
        assert response.status_code == 400, response.content
        # Check that the form has an error for the new password field
        assert "new_password" in response.context["form"].errors
        # Verify password was not changed
        user.refresh_from_db()
        assert not user.check_password("123456")

    def test_rate_limit(
        self,
        user: User,
        password: str,
        user_client: Client,
        resource_url: str,
        faker: Faker,
        settings: Base,
    ) -> None:
        """Test that rate limiting is enforced correctly."""
        settings.RATELIMIT_ENABLE = True

        # Make 5 requests (the limit is 5/h)
        for _ in range(5):
            response = user_client.post(
                resource_url,
                {
                    "current_password": password,
                    "new_password": faker.password(),
                    "new_password_confirm": faker.password(),
                },
                follow=True,
            )
            # These should succeed (even if password validation fails)
            assert response.status_code in [200, 400]

        # The 6th request should be rate limited
        response = user_client.post(
            resource_url,
            {
                "current_password": password,
                "new_password": faker.password(),
                "new_password_confirm": faker.password(),
            },
        )
        assert response.status_code == 429


class TestEmailAddressUpdateDjango:
    """Test django email address update view."""

    @pytest.fixture
    def resource_url(self) -> str:
        """Return URL to this view."""
        return reverse("users-django:update-email-address")

    def test_get_form(self, user_client: Client, resource_url: str) -> None:
        """Test that the form is displayed correctly."""
        response = user_client.get(resource_url)
        assert response.status_code == 200
        assert "form" in response.context

    def test_happy_path(
        self,
        user: User,
        password: str,
        user_client: Client,
        resource_url: str,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Test submitting the form with valid data."""
        old_email = user.email
        new_email = "new-email@example.com"

        with django_assert_num_queries(11):
            response = user_client.post(
                resource_url,
                {
                    "new_email": new_email,
                    "password": password,
                },
                follow=True,
            )
            assert response.status_code == 200

        # Check that we were redirected to the profile page
        assert response.redirect_chain[-1][0] == reverse(
            "users-django:profile"
        )

        # Verify the unconfirmed email was set but the actual email hasn't changed yet
        user.refresh_from_db()
        assert user.email == old_email
        assert user.unconfirmed_email == new_email

    def test_with_incorrect_password(
        self,
        user: User,
        user_client: Client,
        resource_url: str,
    ) -> None:
        """Test submitting the form with an incorrect password."""
        old_email = user.email
        new_email = "new-email@example.com"

        response = user_client.post(
            resource_url,
            {
                "new_email": new_email,
                "password": "wrong-password",
            },
        )

        # Should return to the form with an error
        assert response.status_code == 400
        # Check that the form has an error for the password field
        assert "password" in response.context["form"].errors

        # Verify email was not changed
        user.refresh_from_db()
        assert user.email == old_email

    def test_rate_limit(
        self,
        user: User,
        password: str,
        user_client: Client,
        resource_url: str,
        faker: Faker,
        settings: Base,
    ) -> None:
        """Test that rate limiting is enforced correctly."""
        settings.RATELIMIT_ENABLE = True

        # Make 5 requests (the limit is 5/h)
        for _ in range(5):
            response = user_client.post(
                resource_url,
                {"new_email": faker.email(), "password": password},
                follow=True,
            )
            assert response.status_code == 200

        # The 6th request should be rate limited
        response = user_client.post(
            resource_url,
            {"new_email": faker.email(), "password": password},
        )
        assert response.status_code == 429
        assert user.unconfirmed_email is None

    def test_with_invalid_email(
        self,
        user: User,
        password: str,
        user_client: Client,
        resource_url: str,
    ) -> None:
        """Test submitting the form with an invalid email."""
        old_email = user.email

        response = user_client.post(
            resource_url,
            {
                "new_email": "not-an-email",
                "password": password,
            },
        )

        # Should return to the form with an error
        assert response.status_code == 400
        # Check that the form has an error for the email field
        assert "new_email" in response.context["form"].errors

        # Verify email was not changed
        user.refresh_from_db()
        assert user.email == old_email


# DRF View tests


# Create (not relevant)
# Read
class TestUserRead:
    """Test UserReadUpdate view."""

    @pytest.fixture
    def resource_url(self) -> str:
        """Return URL to this view."""
        return reverse("user:users:read")

    def test_unauthenticated(
        self,
        rest_client: APIClient,
        resource_url: str,
    ) -> None:
        """Assert that we get 200 back even if not logged in."""
        response = rest_client.get(resource_url)
        assert response.status_code == 200, response.data
        assert response.data == {"kind": "unauthenticated"}

    def test_authenticated(
        self,
        rest_user_client: APIClient,
        resource_url: str,
        user: User,
    ) -> None:
        """Assert we can post to this view this while being logged in."""
        response = rest_user_client.get(resource_url)
        assert response.status_code == 200, response.data
        assert response.data == {
            "kind": "authenticated",
            "email": user.email,
            "preferred_name": user.preferred_name,
            "profile_picture": None,
        }


class TestUserUpdate:
    """Test UserReadUpdate view."""

    @pytest.fixture
    def resource_url(self) -> str:
        """Return URL to this view."""
        return reverse("user:users:update")

    def test_update(
        self,
        rest_user_client: APIClient,
        resource_url: str,
        django_assert_num_queries: DjangoAssertNumQueries,
        user: User,
    ) -> None:
        """Test updating."""
        with django_assert_num_queries(5):
            response = rest_user_client.put(
                resource_url,
                data={},
            )
            assert response.status_code == HTTP_200_OK, response.data
        user.refresh_from_db()
        assert user.preferred_name is None
        response = rest_user_client.put(
            resource_url,
            data={"preferred_name": "Locutus of Blorb"},
        )
        assert response.status_code == HTTP_200_OK, response.data
        user.refresh_from_db()
        assert user.preferred_name == "Locutus of Blorb"
        response = rest_user_client.put(
            resource_url,
            data={"preferred_name": ""},
        )
        assert response.status_code == HTTP_200_OK, response.data
        user.refresh_from_db()
        assert user.preferred_name == ""

    def test_update_unauthenticed(
        self,
        rest_client: APIClient,
        resource_url: str,
        user: User,
    ) -> None:
        """Test updating when not authenticated."""
        name = user.preferred_name
        response = rest_client.put(
            resource_url,
            data={"preferred_name": "Here's to the finest crew in Starfleet."},
        )
        assert response.status_code == HTTP_403_FORBIDDEN, response.data
        user.refresh_from_db()
        # Canary in the mines
        assert user.preferred_name == name

    def test_naughty_preferred_name(
        self, rest_user_client: APIClient, resource_url: str, user: User
    ) -> None:
        """Test that we do not allow injecting a domain name."""
        name = user.preferred_name
        response = rest_user_client.put(
            resource_url, data={"preferred_name": "google.com"}
        )
        assert response.status_code == HTTP_400_BAD_REQUEST, response.data
        assert response.data == {
            "status": "invalid",
            "code": 400,
            "details": {},
            "general": "Preferred name can only contain '.' or ':' if "
            "followed by whitespace or if located at the end.",
        }
        user.refresh_from_db()
        # Canary in the mines
        assert user.preferred_name == name


# Delete


# RPC
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
        rest_client: APIClient,
        resource_url: str,
        headers: Headers,
        uploaded_file: File,
    ) -> None:
        """Assert we can't post to this view."""
        response = rest_client.post(
            resource_url,
            {"file": uploaded_file},
            format="multipart",
            **headers,
        )

        assert response.status_code == 403, response.data

    def test_authenticated(
        self,
        rest_user_client: APIClient,
        resource_url: str,
        headers: Headers,
        uploaded_file: File,
        user: User,
    ) -> None:
        """Test setting and then clearing a picture."""
        response = rest_user_client.post(
            resource_url,
            {"file": uploaded_file},
            format="multipart",
            **headers,
        )
        assert response.status_code == 204, response.data
        user.refresh_from_db()
        assert user.profile_picture is not None
        # Now clear it
        response = rest_user_client.post(
            resource_url,
            {},
            format="multipart",
        )
        assert response.status_code == 204, response.data
        user.refresh_from_db()
        assert not user.profile_picture


@pytest.mark.django_db
class TestChangePassword:
    """Test changing password using API."""

    @pytest.fixture
    def resource_url(self) -> str:
        """Return URL to this view."""
        return reverse("user:users:change-password")

    def test_with_correct_password(
        self,
        user: User,
        password: str,
        rest_user_client: APIClient,
        resource_url: str,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Test changing password with a good password."""
        # 1 for changing the password
        # 7 for session update
        # 2 for email send
        with django_assert_num_queries(14):
            response = rest_user_client.post(
                resource_url,
                data={
                    "current_password": password,
                    "new_password": "hello-world123",
                },
            )
            assert response.status_code == 204, response.data
        assert response.wsgi_request.user.is_authenticated
        user.refresh_from_db()
        assert user.check_password("hello-world123")


@pytest.mark.django_db
class TestRequestEmailAddressUpdate:
    """Test requesting an email address update token."""

    @pytest.fixture
    def resource_url(self) -> str:
        """Return URL to this view."""
        return reverse("user:users:request-email-address-update")

    def test_happy_path(
        self,
        user: User,
        password: str,
        rest_user_client: APIClient,
        resource_url: str,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Test sending the correct data."""
        old_email = user.email
        new_email = "henlo-wolrd@example.com"
        with django_assert_num_queries(7):
            response = rest_user_client.post(
                resource_url,
                data={"new_email": new_email, "password": password},
            )
            assert response.status_code == 204, response.data
        user.refresh_from_db()
        assert user.email == old_email  # i.e., nothing changed
        assert user.unconfirmed_email == new_email


@pytest.mark.django_db
class TestConfirmEmailAddressUpdate:
    """Test confirming the email address."""

    @pytest.fixture
    def resource_url(self) -> str:
        """Return URL to this view."""
        return reverse("user:users:confirm-email-address-update")

    def test_happy_path(
        self,
        user: User,
        rest_user_client: APIClient,
        resource_url: str,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Test that the email address is updated."""
        user.unconfirmed_email = "new-email@example.com"
        user.save()
        token = user_make_token(user=user, kind="update_email_address")
        # Went up from 6 -> 8
        # seems like something around the user name validation or savepoint
        # logic changed:
        # SAVEPOINT "s140360466458432_x51"
        #
        # SELECT 1 AS "a" FROM "user_user" WHERE ("user_user"."email" = 'new-email@example.com' AND NOT ("user_user"."id" = 8)) LIMIT 1
        #
        # SAVEPOINT "s140360466458432_x52"
        #
        # SELECT 1 AS "_check" WHERE COALESCE(('Chase Moore'::text ~  E'^([.:]\\s|[^.:])*[.:]?$'), true)
        #
        # RELEASE SAVEPOINT "s140360466458432_x52"
        #
        # UPDATE "user_user" SET "password" = 'pbkdf2_sha256$1000000$viwTzJ3svHyVJM2hTWHqNi$oq1K3ZSX2NuDkrgcH61k5enwUws8rV9t1I9aXgkspSQ=', "last_login" = NULL, "created" = '2025-05-30 08:00:39.436426+00:00'::timestamptz, "modified" = '2025-05-30 08:00:39.442602+00:00'::timestamptz, "email" = 'new-email@example.com', "unconfirmed_email" = 'new-email@example.com', "is_staff" = false, "is_superuser" = false, "is_active" = true, "profile_picture" = '', "preferred_name" = 'Chase Moore', "tos_agreed" = NULL, "privacy_policy_agreed" = NULL WHERE "user_user"."id" = 8
        #
        # INSERT INTO "user_previousemailaddress" ("created", "modified", "user_id", "email") VALUES ('2025-05-30 08:00:39.442925+00:00'::timestamptz, '2025-05-30 08:00:39.442930+00:00'::timestamptz, 8, 'millerjill@example.org') RETURNING "user_previousemailaddress"."id"
        #
        # RELEASE SAVEPOINT "s140360466458432_x51"
        with django_assert_num_queries(8):
            response = rest_user_client.post(
                resource_url,
                data={"confirmation_token": token},
            )
            assert response.status_code == 204, response.data
        user.refresh_from_db()
        assert user.email == "new-email@example.com"
