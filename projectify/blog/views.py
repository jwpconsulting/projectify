# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2026 JWP Consulting GK
"""Blog views."""

import logging
from pathlib import Path
from typing import Optional
from uuid import uuid4

from django import forms
from django.core.files.storage import default_storage
from django.core.files.uploadedfile import UploadedFile
from django.forms.utils import ErrorList
from django.http import (
    Http404,
    HttpRequest,
    HttpResponse,
    HttpResponseForbidden,
    JsonResponse,
)
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_http_methods

from django_sendfile import sendfile

from projectify.lib.settings import get_settings
from projectify.lib.types import AuthenticatedHttpRequest
from projectify.lib.utils import get_image_format
from projectify.lib.views import platform_view

from .selectors.post import post_find_by_slug, post_list_published

logger = logging.getLogger(__name__)


def post_list(request: HttpRequest) -> HttpResponse:
    """Display list of blog posts."""
    posts = post_list_published()
    context = {"posts": posts}
    return render(request, "blog/post_list.html", context)


def post_detail(request: HttpRequest, slug: str) -> HttpResponse:
    """Display a single blog post."""
    post = post_find_by_slug(slug=slug)
    if not post:
        raise Http404(_("Post with slug {slug} not found").format(slug=slug))
    recent = post_list_published(exclude=post)[:5]
    context = {"post": post, "recent_posts": recent}
    return render(request, "blog/post_detail.html", context)


def sanitize_blog_picture_path(picture_name: str) -> Optional[str]:
    """Sanitize a path reference to a blog picture upload."""
    if "/" in picture_name:
        return None
    # As if that wasn't enough, let's imagine we're on Michælsoft Binbows
    if "\\" in picture_name:
        return None
    return str(Path("blog") / picture_name)


def serve_picture(request: HttpRequest, name: str) -> HttpResponse:
    """Serve a blog picture using sendfile."""
    full_path = sanitize_blog_picture_path(name)
    if full_path is None or not default_storage.exists(str(full_path)):
        logger.warning("Picture with name %s not found at %s", name, full_path)
        raise Http404(_("Picture {name} not found").format(name=name))
    file_path = default_storage.path(str(full_path))
    return sendfile(request, file_path)


# SPDX-SnippetBegin
# SPDX-License-Identifier: MIT
# SPDX-SnippetCopyrightText: 2022 LOGIC SMPC <paris@withlogic.co>


class UploadAttachmentForm(forms.Form):
    """Form for uploading blog post attachments."""

    file = forms.FileField()

    def clean_file(self) -> UploadedFile:
        """Validate file size and type."""
        file: UploadedFile = self.cleaned_data["file"]
        settings = get_settings()

        size = file.size
        max_size = settings.BLOG_ALLOWED_FILE_SIZE
        if size > max_size:
            raise forms.ValidationError(
                _("Files too large: {size} KiB. Max: {max_size} KiB").format(
                    size=size // 1024, max_size=max_size // 1024
                )
            )

        # Use Pillow to detect actual image format
        image_format = get_image_format(file)
        allowed = settings.BLOG_ALLOWED_FILE_TYPES
        if image_format not in allowed:
            raise forms.ValidationError(
                _(
                    "{image_format} is not one of the allowed file types: {allowed}"
                ).format(image_format=image_format, allowed=allowed)
            )

        return file


@platform_view
@require_http_methods(["POST"])
def upload_attachment(request: AuthenticatedHttpRequest) -> HttpResponse:
    """Upload an attachment."""
    if not request.user.is_superuser:
        return HttpResponseForbidden()

    form = UploadAttachmentForm(request.POST, request.FILES)
    if not form.is_valid():
        errors: Optional[ErrorList] = form.errors.get("file")
        error_message: object = (
            errors.get_json_data() if errors else _("No error message")
        )
        return JsonResponse({"error": error_message}, status=400)

    attachment: UploadedFile = form.cleaned_data["file"]
    attachment_name = Path(attachment.name)
    upload_name = (
        f"{uuid4()}.{attachment_name.name[:8]}{attachment_name.suffix}"
    )
    upload_path = Path("blog") / upload_name
    default_storage.save(str(upload_path), attachment)
    url = reverse("blog:serve_picture", args=(upload_name,))
    return JsonResponse({"url": url}, status=201)


# SPDX-SnippetEnd
