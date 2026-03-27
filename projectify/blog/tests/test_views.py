# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2022, 2026 JWP Consulting GK
"""Test blog views."""

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client
from django.urls import reverse

import pytest

from ..models import Post

pytestmark = pytest.mark.django_db


def test_post_list_displays_posts(client: Client, post: Post) -> None:
    """Test that post list displays posts."""
    response = client.get(reverse("blog:post_list"))
    assert response.status_code == 200
    assert post.title in response.content.decode()


def test_post_detail_displays_post(client: Client, post: Post) -> None:
    """Test that post detail displays a post."""
    response = client.get(reverse("blog:post_detail", args=[post.slug]))
    assert response.status_code == 200
    assert post.title in response.content.decode()


def test_upload_attachment_superuser_can_upload(
    superuser_client: Client,
    uploaded_file: SimpleUploadedFile,
) -> None:
    """Test that superuser can upload files."""
    response = superuser_client.post(
        reverse("blog:upload_attachment"), {"file": uploaded_file}
    )
    assert response.status_code == 201, response.content
    assert "url" in response.json()


def test_upload_attachment_regular_user_cannot_upload(
    user_client: Client, uploaded_file: SimpleUploadedFile
) -> None:
    """Test that regular users cannot upload files."""
    response = user_client.post(
        reverse("blog:upload_attachment"), {"file": uploaded_file}
    )
    assert response.status_code == 403


def test_upload_attachment_anonymous_user_cannot_upload(
    client: Client, uploaded_file: SimpleUploadedFile
) -> None:
    """Test that anonymous users cannot upload files."""
    response = client.post(
        reverse("blog:upload_attachment"), {"file": uploaded_file}
    )
    assert response.status_code == 302


def test_upload_attachment_rejects_invalid_file_types(
    superuser_client: Client,
) -> None:
    """Test that upload rejects files not in the allowlist."""
    invalid_file = SimpleUploadedFile(
        "test.txt",
        b"This is a text file",
        content_type="text/plain",
    )
    response = superuser_client.post(
        reverse("blog:upload_attachment"), {"file": invalid_file}
    )
    assert response.status_code == 400, response.content
    assert b"not one of the allowed file types" in response.content
