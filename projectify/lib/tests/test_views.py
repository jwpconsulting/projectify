# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2026 JWP Consulting GK
"""Test lib views."""

from django.test.client import Client
from django.urls import reverse

import pytest


class TestColoredIconView:
    """Test the colored_icon view."""

    def test_get(self, client: Client) -> None:
        """Test getting an icon. Only test for one color."""
        url = reverse(
            "colored-icon",
            kwargs={"icon": "external_links", "color": "primary"},
        )
        response = client.get(url)

        assert response.status_code == 200
        assert response["Content-Type"] == "image/svg+xml"
        assert '<svg style="color: #2563EB' in response.content.decode()

    @pytest.mark.parametrize(
        ("icon", "color"),
        [
            ("made-up", "primary"),
            ("external_links", "wrong-color"),
            ("made-up", "wrong-color"),
        ],
    )
    def test_not_found(self, client: Client, icon: str, color: str) -> None:
        """Test that 404 is returned for invalid icon or color."""
        url = reverse(
            "colored-icon",
            kwargs={"icon": icon, "color": color},
        )
        assert client.get(url).status_code == 404
