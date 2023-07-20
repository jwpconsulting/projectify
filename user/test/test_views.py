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

from .. import (
    models,
)


Headers = Mapping[str, Any]


@pytest.mark.django_db
class TestProfilePictureUploadView:
    """Test ProfilePictureUploadView."""

    @pytest.fixture
    def resource_url(self) -> str:
        """Return URL to this view."""
        return reverse("user:profile-picture-upload")

    @pytest.fixture
    def headers(self, png_image: File) -> Headers:
        """Return headers."""
        return {
            "HTTP_CONTENT_DISPOSITION": "attachment; filename=test.png",
            "HTTP_CONTENT_LENGTH": len(png_image),
        }

    def test_unauthenticated(
        self, client: Client, resource_url: str, headers: Headers
    ) -> None:
        """Assert we can't view this while being logged out."""
        response = client.post(resource_url, **headers)
        assert response.status_code == 403, response.content

    def test_authenticated(
        self,
        user_client: Client,
        resource_url: str,
        headers: Headers,
        uploaded_file: File,
        user: models.User,
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


@pytest.mark.django_db
class TestUserRetrieve:
    """Test UserRetrieve view."""

    @pytest.fixture
    def resource_url(self) -> str:
        """Return URL to this view."""
        return reverse("user:user")

    def test_authenticated(
        self, user_client: Client, resource_url: str, user: models.User
    ) -> None:
        """Assert we can post to this view this while being logged in."""
        response = user_client.get(resource_url)
        assert response.status_code == 200, response.content
