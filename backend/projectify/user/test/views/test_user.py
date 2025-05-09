# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2022, 2023 JWP Consulting GK
"""User view tests."""

from collections.abc import Mapping
from typing import Any

from django.core.files import File
from django.urls import reverse

import pytest
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_403_FORBIDDEN,
)
from rest_framework.test import APIClient

from projectify.user.services.internal import user_make_token
from pytest_types import DjangoAssertNumQueries

from ...models import User

pytestmark = pytest.mark.django_db

Headers = Mapping[str, Any]


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
        with django_assert_num_queries(3):
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
        with django_assert_num_queries(12):
            response = rest_user_client.post(
                resource_url,
                data={
                    "current_password": password,
                    "new_password": "hello-world123",
                },
            )
            assert response.status_code == 204, response.data
        # Assert that we stay logged in, i.e., sessionid still in cookies
        assert "sessionid" in response.cookies
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
        with django_assert_num_queries(5):
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
        with django_assert_num_queries(6):
            response = rest_user_client.post(
                resource_url,
                data={"confirmation_token": token},
            )
            assert response.status_code == 204, response.data
        user.refresh_from_db()
        assert user.email == "new-email@example.com"
