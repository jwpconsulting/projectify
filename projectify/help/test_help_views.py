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
    """Test help list view returns 200 and contains expected content."""
    url = reverse("help:list")
    response = client.get(url)

    assert response.status_code == 200
    content = response.content.decode()
    assert "Basics" in content
    assert "Workspaces" in content


@pytest.mark.parametrize("page_key", HELP_TOPICS.keys())
def test_help_detail_view_valid_pages(client: Client, page_key: str) -> None:
    """Test help detail view for all valid pages."""
    url = reverse("help:detail", args=(page_key,))
    response = client.get(url)

    assert response.status_code == 200
    content = response.content.decode()
    topic = HELP_TOPICS[page_key]
    assert str(topic["title"]) in content
    assert "Table of Contents" in content
    assert 'class="toc' in content


def test_help_detail_view_invalid_page(client: Client) -> None:
    """Test help detail view returns 404 for invalid page."""
    url = reverse("help:detail", args=("nonexistent",))
    assert client.get(url).status_code == 404
