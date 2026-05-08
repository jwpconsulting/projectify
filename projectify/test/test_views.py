# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2026 JWP Consulting GK
"""Test general views."""

import logging

from django.test.client import Client
from django.urls import reverse

import pytest


class TestHealthCheck:
    """Test health check view."""

    def test_health_check_returns_204(self, client: Client) -> None:
        """Test that health check endpoint returns 204 No Content."""
        response = client.get(reverse("health-check"))
        assert response.status_code == 204
        assert response.content == b""


@pytest.mark.django_db
class TestSitemap:
    """Test the Projectify view."""

    def test_sitemap(self, client: Client) -> None:
        """Test that the sitemap works."""
        # Not using reverse here because crawlers commonly assume
        # sitemap.xml exists. Then, the sitemap being at sitemap.xml is part
        # of the spec.
        assert client.get("/sitemap.xml").status_code == 200


class Test404NotFound:
    """Test the 404 not found view."""

    def test_404(
        self, client: Client, caplog: pytest.LogCaptureFixture
    ) -> None:
        """Check log output for 404 handler."""
        with caplog.at_level(logging.WARNING, logger="projectify.views"):
            response = client.get("/this-page-does-not-exist/")
            assert response.status_code == 404
            assert b"Page not found" in response.content

        assert "Received Resolver404 exception for 404 error" in caplog.text
