"""User view tests."""
import base64

from django.core.files.uploadedfile import (
    SimpleUploadedFile,
)
from django.urls import (
    reverse,
)

import pytest


@pytest.mark.django_db
class TestProfilePictureUploadView:
    """Test ProfilePictureUploadView."""

    image = base64.b64decode(
        "iVBORw0KGgoAAAANSUhEUgAAACAAAAAgAgAAAAAcoT2JAAAABGdBTUEAAYagMeiWX\
        wAAAB9JREFUeJxjYAhd9R+M8TCIUMIAU4aPATMJH2OQuQcAvUl/gYsJiakAAAAASUVORK5\
        CYII="
    )

    @pytest.fixture
    def uploaded_file(self):
        """Return uploaded file."""
        return SimpleUploadedFile("test.png", self.image)

    @pytest.fixture
    def resource_url(self):
        """Return URL to this view."""
        return reverse("user:profile-picture-upload")

    @pytest.fixture
    def headers(self):
        """Return headers."""
        return {
            "HTTP_CONTENT_DISPOSITION": "attachment; filename=test.png",
            "HTTP_CONTENT_LENGTH": len(self.image),
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
