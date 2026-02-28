# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2026 JWP Consulting GK
"""Test avatar marble view."""

from uuid import uuid4

from django.test import Client
from django.urls import reverse

import pytest

from pytest_types import DjangoAssertNumQueries

from ...models import TeamMember

pytestmark = pytest.mark.django_db


@pytest.fixture
def resource_url(team_member: TeamMember) -> str:
    """Return URL to this view."""
    return reverse("dashboard:avatar-marble", args=[team_member.uuid])


def test_response(
    user_client: Client,
    resource_url: str,
    django_assert_num_queries: DjangoAssertNumQueries,
    team_member: TeamMember,
) -> None:
    """Test that view returns a valid, cached SVG."""
    with django_assert_num_queries(3):
        response = user_client.get(resource_url)
    assert response.status_code == 200
    assert response["Content-Type"] == "image/svg+xml"
    assert f"<title>{team_member.user}</title>" in response.content.decode()
    assert "max-age=3600" in response["Cache-Control"]
    # Test that it's deterministic
    assert response.content == user_client.get(resource_url).content


def test_nonexistent_team_member_returns_404(user_client: Client) -> None:
    """Test that nonexistent team member returns 404."""
    assert (
        user_client.get(
            reverse("dashboard:avatar-marble", args=(uuid4(),))
        ).status_code
        == 404
    )
