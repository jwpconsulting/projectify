# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2026 JWP Consulting GK
"""Blog views."""

from datetime import datetime
from uuid import uuid4

from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.uploadedfile import UploadedFile
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseForbidden,
    JsonResponse,
)
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_http_methods

from projectify.lib.types import AuthenticatedHttpRequest
from projectify.lib.views import platform_view

from .models import Post


def post_list(request: HttpRequest) -> HttpResponse:
    """Display list of blog posts."""
    posts = Post.objects.select_related("body").order_by("-published")
    context = {"posts": posts}
    return render(request, "blog/post_list.html", context)


def post_detail(request: HttpRequest, slug: str) -> HttpResponse:
    """Display a single blog post."""
    post = get_object_or_404(Post.objects.select_related("body"), slug=slug)
    recent = Post.objects.select_related("body").order_by("-published")[:5]
    context = {"post": post, "recent_posts": recent}
    return render(request, "blog/post_detail.html", context)


# SPDX-SnippetBegin
# SPDX-License-Identifier: MIT
# SPDX-SnippetCopyrightText: 2022 LOGIC SMPC <paris@withlogic.co>

ALLOWED_FILE_SIZE = getattr(settings, "PROSE_ATTACHMENT_ALLOWED_FILE_SIZE", 5)


def validate_file(file: UploadedFile) -> bool:
    """Validate file size."""
    file_size: float = file.size / 1024 / 1024
    return file_size <= ALLOWED_FILE_SIZE


@platform_view
@require_http_methods(["POST"])
def upload_attachment(request: AuthenticatedHttpRequest) -> HttpResponse:
    """Upload an attachment."""
    if not request.user.is_superuser:
        return HttpResponseForbidden()

    attachment = request.FILES.get("file")
    if not attachment:
        return HttpResponseBadRequest()
    if not validate_file(attachment):
        return JsonResponse(
            {"error": f"Files must be {ALLOWED_FILE_SIZE}MB or smaller."},
            status=400,
        )
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
