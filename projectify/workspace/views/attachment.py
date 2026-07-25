# SPDX-License-Identifier: AGPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 JWP Consulting GK
"""Workspace attachment views."""

import logging
from uuid import UUID

from django.core.files.storage import default_storage
from django.core.files.uploadedfile import UploadedFile
from django.forms.utils import ErrorList
from django.http import Http404, HttpResponse, JsonResponse
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_GET, require_POST

from django_sendfile import sendfile

from projectify.lib.types import AuthenticatedHttpRequest
from projectify.lib.views import platform_view
from projectify.workspace.selectors.attachment import (
    attachment_find_by_workspace_uuid_and_name,
)
from projectify.workspace.selectors.team_member import (
    team_member_find_by_workspace_uuid,
)
from projectify.workspace.services.attachment import attachment_create

from ..forms import AttachmentUploadForm

logger = logging.getLogger(__name__)


@platform_view
@require_POST
def attachment_create_view(
    request: AuthenticatedHttpRequest, ws_uuid: UUID
) -> HttpResponse:
    """Upload an image attachment to a workspace."""
    team_member = team_member_find_by_workspace_uuid(
        workspace_uuid=ws_uuid, who=request.user
    )
    if team_member is None:
        raise Http404(
            _(
                "Could not find workspace with UUID {workspace_uuid} for current user"
            ).format(workspace_uuid=ws_uuid)
        )
    form = AttachmentUploadForm(request.POST, request.FILES)
    if not form.is_valid():
        match form.errors.get("file"):
            case None:
                error: str | list[dict[str, str]] = _("No error message")
            case ErrorList() as e:
                error = e.get_json_data()
        return JsonResponse({"error": error}, status=400)

    file: UploadedFile = form.cleaned_data["file"]
    attachment = attachment_create(who=team_member, file=file)
    url = attachment.get_absolute_url()
    return JsonResponse({"url": url}, status=201)


@platform_view
@require_GET
def attachment_view(
    request: AuthenticatedHttpRequest, ws_uuid: UUID, name: str
) -> HttpResponse:
    """Retrieve an attachment with sendfile()."""
    attachment = attachment_find_by_workspace_uuid_and_name(
        who=request.user, name=name, workspace_uuid=ws_uuid
    )
    if attachment is None:
        raise Http404(
            _("Could not find workspace with UUID {workspace_uuid}").format(
                workspace_uuid=ws_uuid
            )
        )
    # this view could check whether the file exists. An Attachment record
    # existing but the file not being there is unexpected so I'd rather
    # let it crash hard
    file_path = default_storage.path(str(attachment.storage_path))
    return sendfile(request, file_path)
