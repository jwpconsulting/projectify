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

from ...models import User

Headers = Mapping[str, Any]


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
