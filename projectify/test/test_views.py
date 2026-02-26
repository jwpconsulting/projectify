# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2026 JWP Consulting GK
"""Test general views."""

from django.test import TestCase
from django.urls import reverse


class TestHealthCheck(TestCase):
    """Test health check view."""

    def test_health_check_returns_204(self) -> None:
        """Test that health check endpoint returns 204 No Content."""
        response = self.client.get(reverse("health-check"))
        assert response.status_code == 204
        assert response.content == b""
