# SPDX-License-Identifier: AGPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 JWP Consulting GK
"""Test attachment views."""

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client
from django.urls import reverse

import pytest

from ...models import Attachment, TeamMember

pytestmark = pytest.mark.django_db


@pytest.fixture
def create_url(team_member: TeamMember) -> str:
    """Return this view's URL."""
    ws_uuid = team_member.workspace.uuid
    return reverse("dashboard:attachments:create", args=(ws_uuid,))


def test_upload(
    user_client: Client,
    uploaded_file: SimpleUploadedFile,
    png_image: bytes,
    create_url: str,
) -> None:
    """Test uploading an attachment."""
    response = user_client.post(create_url, {"file": uploaded_file})
    assert response.status_code == 201, response.content
    data = response.json()
    assert "url" in data

    serve_response = user_client.get(data["url"])
    assert serve_response.status_code == 200
    assert serve_response.content == png_image


def test_view_authorized(
    user_client: Client, attachment: Attachment, png_image: bytes
) -> None:
    """Test viewing as an authorized user."""
    serve_response = user_client.get(attachment.get_absolute_url())
    assert serve_response.status_code == 200
    assert serve_response.content == png_image


def test_view_bad_path(
    user_client: Client, attachment: Attachment, png_image: bytes
) -> None:
    """Test viewing as an authorized user."""
    url = reverse(
        "dashboard:attachments:view",
        args=(attachment.workspace.uuid, "wrong-name.png"),
    )
    serve_response = user_client.get(url)
    assert serve_response.status_code == 404
    assert serve_response.content != png_image


def test_view_deleted_attachment(
    user_client: Client, attachment: Attachment, png_image: bytes
) -> None:
    """Test viewing as an authorized user."""
    url = attachment.get_absolute_url()
    attachment.delete()
    serve_response = user_client.get(url)
    assert serve_response.status_code == 404
    assert serve_response.content != png_image


def test_view_unauthorized(
    unrelated_user_client: Client, attachment: Attachment, png_image: bytes
) -> None:
    """Test what happens when you try to view files from another ws."""
    not_found_response = unrelated_user_client.get(
        attachment.get_absolute_url()
    )
    assert not_found_response.status_code == 404
    assert not_found_response.content != png_image


# TODO test path traversal
