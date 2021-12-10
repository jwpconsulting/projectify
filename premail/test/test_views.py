"""Test premail views."""
from django.urls import (
    reverse,
)

import pytest


@pytest.mark.django_db
class TestEmailList:
    """Test EmailList."""

    @pytest.fixture
    def resource_url(self):
        """Return URL to this view."""
        return reverse("premail:email-list")

    def test_non_superuser(self, user_client, resource_url):
        """Assert we can't view this while being a normal user."""
        response = user_client.get(resource_url)
        assert response.status_code == 403

    def test_superuser(self, superuser_client, resource_url):
        """Assert we can view this while being a super user."""
        response = superuser_client.get(resource_url)
        assert response.status_code == 200


@pytest.mark.django_db
class TestEmailPreview:
    """Test EmailPreview."""

    @pytest.fixture
    def resource_url(self):
        """Return URL to this view."""
        return reverse("premail:email-preview", kwargs={"slug": "SampleEmail"})

    def test_non_superuser(self, user_client, resource_url):
        """Assert we can't view this while being a normal user."""
        response = user_client.get(resource_url)
        assert response.status_code == 403

    def test_superuser(self, superuser_client, resource_url):
        """Assert we can view this while being a super user."""
        response = superuser_client.get(resource_url)
        assert response.status_code == 200
