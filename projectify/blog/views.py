# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2026 JWP Consulting GK
"""Blog views."""

from datetime import datetime
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
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_http_methods

from projectify.lib.settings import get_settings
from projectify.lib.types import AuthenticatedHttpRequest
from projectify.lib.utils import get_image_format
from projectify.lib.views import platform_view

from .selectors.post import post_find_by_slug, post_list_published


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

    attachment = form.cleaned_data["file"]
    attachment_dir = datetime.now().strftime("%Y/%m/%d")
    attachment_id = uuid4()
    attachment_extension = attachment.name.split(".")[-1]
    key = f"{attachment_dir}/{attachment_id}.{attachment_extension}"
    path = f"prose/{key}"
    default_storage.save(path, attachment)
    payload = {
        "url": default_storage.url(path),
    }
    return JsonResponse(payload, status=201)


# SPDX-SnippetEnd
