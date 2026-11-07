# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2026 JWP Consulting GK
"""Test help views."""

from django.test import Client
from django.urls import reverse

import pytest

from projectify.help.views import HELP_TOPICS

pytestmark = pytest.mark.django_db


def test_help_list_view(client: Client) -> None:
    """Test help list view."""
    url = reverse("help:list")
    response = client.get(url)
    assert response.status_code == 200
    assert "Basics" in response.content.decode()
    assert "Workspaces" in response.content.decode()


@pytest.mark.parametrize("k,v", HELP_TOPICS.items())
def test_help_detail_view(client: Client, k: str, v: dict[str, str]) -> None:
    """Test help detail view."""
    url = reverse(f"help:topic:{k}")
    response = client.get(url)
    assert response.status_code == 200
    assert str(v["title"]) in response.content.decode()
    assert "Table of Contents" in response.content.decode()
    assert 'class="toc' in response.content.decode()
