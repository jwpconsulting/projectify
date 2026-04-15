# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2022, 2026 JWP Consulting GK
"""Test blog views."""

from django.core.files.storage import default_storage
from django.core.files.uploadedfile import SimpleUploadedFile, UploadedFile
from django.test import Client
from django.urls import reverse

import pytest

from ..models import Post
from ..views import sanitize_blog_picture_path

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


def test_post_detail_not_found(client: Client) -> None:
    """Test retrieving a non-existing post."""
    response = client.get(reverse("blog:post_detail", args=["bla"]))
    assert response.status_code == 404


def test_post_detail_redirect(client: Client, post: Post) -> None:
    """Test that slug without trailing slash redirects permanently."""
    url = reverse("blog:post_detail", args=[post.slug])
    response = client.get(f"{url}/")
    assert response.status_code == 301
    assert response["Location"] == url


def test_uploading_attachments(
    superuser_client: Client, uploaded_file: UploadedFile, png_image: bytes
) -> None:
    """Test that superuser can upload files and view them, too."""
    url = reverse("blog:upload_attachment")
    response = superuser_client.post(url, {"file": uploaded_file})
    assert response.status_code == 201, response.content
    data = response.json()
    assert "url" in data

    # Based on the URL, view the contents
    serve_response = superuser_client.get(data["url"])
    assert serve_response.status_code == 200
    assert serve_response.content == png_image


def test_upload_attachment_regular_user_cannot_upload(
    user_client: Client, uploaded_file: UploadedFile
) -> None:
    """Test that regular users cannot upload files."""
    url = reverse("blog:upload_attachment")
    response = user_client.post(url, {"file": uploaded_file})
    assert response.status_code == 403


def test_upload_attachment_anonymous_user_cannot_upload(
    client: Client, uploaded_file: UploadedFile
) -> None:
    """Test that anonymous users cannot upload files."""
    url = reverse("blog:upload_attachment")
    response = client.post(url, {"file": uploaded_file})
    assert response.status_code == 302


def test_upload_attachment_rejects_invalid_file_types(
    superuser_client: Client,
) -> None:
    """Test that upload rejects files not in the allowlist."""
    invalid_file = SimpleUploadedFile(
        "test.txt", b"This is a text file", content_type="text/plain"
    )
    url = reverse("blog:upload_attachment")
    response = superuser_client.post(url, {"file": invalid_file})
    assert response.status_code == 400, response.content
    assert b"Upload must be one of the" in response.content


def test_post_feed_accessible(client: Client, post: Post) -> None:
    """Test that the RSS feed is accessible."""
    response = client.get(reverse("blog:feed"))
    assert response.status_code == 200
    assert post.title in response.content.decode()
    assert post.author in response.content.decode()


def test_serve_picture(
    client: Client, uploaded_file: UploadedFile, png_image: bytes
) -> None:
    """Test that serve_picture returns an uploaded file."""
    # Missing file
    response = client.get(reverse("blog:serve_picture", args=("file.jpg",)))
    assert response.status_code == 404

    # Existing file
    test_path = "blog/test.jpg"
    default_storage.save(test_path, uploaded_file)

    url = reverse("blog:serve_picture", args=("test.jpg",))
    response = client.get(url)
    assert response.status_code == 200
    assert response.content == png_image

    # Path traverse
    # Try to access ../blog/test.jpg
    traverse_1_url = url.replace("test.jpg", "../{test_path}")
    response = client.get(traverse_1_url)
    assert response.status_code == 404
    assert response.content != png_image

    # Try to access ../test.jpg
    traverse_path = "test.jpg"
    default_storage.save(traverse_path, uploaded_file)
    traverse_2_url = url.replace("test.jpg", "../test.jpg")
    response = client.get(traverse_2_url)
    assert response.status_code == 404
    assert response.content != png_image


def test_sanitize_blog_picture_path() -> None:
    """Test that path traversal attempts are rejected."""
    result = sanitize_blog_picture_path("test.jpg")
    assert result == "blog/test.jpg"
    result = sanitize_blog_picture_path("test..jpg")
    assert result == "blog/test..jpg"
    result = sanitize_blog_picture_path("../test.jpg")
    assert result is None
    result = sanitize_blog_picture_path("../../etc/passwd")
    assert result is None
    result = sanitize_blog_picture_path("subdir/../test.jpg")
    assert result is None
