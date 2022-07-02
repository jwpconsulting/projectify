"""User view tests."""
from django.urls import (
    reverse,
)

import pytest


@pytest.mark.django_db
class TestProfilePictureUploadView:
    """Test ProfilePictureUploadView."""

    @pytest.fixture
    def resource_url(self):
        """Return URL to this view."""
        return reverse("user:profile-picture-upload")

    @pytest.fixture
    def headers(self, png_image):
        """Return headers."""
        return {
            "HTTP_CONTENT_DISPOSITION": "attachment; filename=test.png",
            "HTTP_CONTENT_LENGTH": len(png_image),
        }

    def test_unauthenticated(self, client, resource_url, headers):
        """Assert wecan't view this while being logged out."""
        response = client.post(resource_url, **headers)
        assert response.status_code == 403, response.content

    def test_authenticated(
        self,
        user_client,
        resource_url,
        headers,
        uploaded_file,
        user,
    ):
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
    def resource_url(self):
        """Return URL to this view."""
        return reverse("user:user")

    def test_authenticated(self, user_client, resource_url, user):
        """Assert we can post to this view this while being logged in."""
        response = user_client.get(resource_url)
        assert response.status_code == 200, response.content
