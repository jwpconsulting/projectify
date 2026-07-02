# SPDX-License-Identifier: AGPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 JWP Consulting GK
"""Workspace wiki views."""

import logging
from typing import Any
from uuid import UUID

from django import forms
from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_GET, require_http_methods

from projectify.lib.forms import RichTextEditor
from projectify.lib.types import AuthenticatedHttpRequest
from projectify.lib.views import platform_view
from projectify.workspace.const import TASK_EDITOR_MIN_HEIGHT_CLASS

from ..models import WikiPage, Workspace
from ..selectors.wiki import wiki_find_by_workspace_and_page_title
from ..selectors.workspace import workspace_find_by_workspace_uuid
from ..services.wiki import wiki_page_get_or_create_index

logger = logging.getLogger(__name__)


@platform_view
@require_GET
def wiki_index(
    request: AuthenticatedHttpRequest, ws_uuid: UUID
) -> HttpResponse:
    """Return the default Wiki index page."""
    ws = workspace_find_by_workspace_uuid(
        who=request.user, workspace_uuid=ws_uuid
    )
    if ws is None:
        raise Http404(_("Workspace not found"))
    page = wiki_page_get_or_create_index(workspace=ws, who=request.user)
    context = {"page": page, "workspace": page.workspace}
    return render(request, "workspace/wiki_page_detail.html", context=context)


@platform_view
@require_GET
def wiki_page_view(
    request: AuthenticatedHttpRequest, ws_uuid: UUID, page_title: str
) -> HttpResponse:
    """Upload an image attachment to a workspace."""
    page = wiki_find_by_workspace_and_page_title(
        ws_uuid=ws_uuid, who=request.user, title=page_title
    )
    if page is None:
        raise Http404(
            _("Couldn't find wiki page {title}").format(title=page_title)
        )
    context = {"page": page, "workspace": page.workspace}
    return render(request, "workspace/wiki_page_detail.html", context=context)


class WikiPageForm(forms.ModelForm):
    """Form for WikiPage."""

    def __init__(self, *args: Any, workspace: Workspace, **kwargs: Any):
        """Populate available assignees and optionally set autofocus."""
        super().__init__(*args, **kwargs)
        editor = RichTextEditor(
            heading_blocks=False,
            upload_url=reverse(
                "dashboard:attachments:create", args=(workspace.uuid,)
            ),
            attrs={
                "expand": True,
                "placeholder": _("Enter a description for your task"),
                "class": TASK_EDITOR_MIN_HEIGHT_CLASS,
                "data-suggest-projects-url": reverse(
                    "dashboard:workspaces:suggest-links-project",
                    args=(workspace.uuid,),
                ),
                "data-suggest-links-url": (
                    reverse(
                        "dashboard:workspaces:suggest-links-task",
                        args=(workspace.uuid,),
                    ),
                ),
            },
        )
        self.fields["content"].widget = editor

    class Meta:
        """Meta."""

        model = WikiPage
        fields = "title", "content"


@platform_view
@require_http_methods(["GET", "POST"])
def wiki_page_edit(
    request: AuthenticatedHttpRequest, ws_uuid: UUID, page_title: str
) -> HttpResponse:
    """Upload an image attachment to a workspace."""
    page = wiki_find_by_workspace_and_page_title(
        ws_uuid=ws_uuid, who=request.user, title=page_title
    )
    if page is None:
        raise Http404(
            _("Couldn't find wiki page {title}").format(title=page_title)
        )
    match request.method:
        case "POST":
            form = WikiPageForm(
                workspace=page.workspace, instance=page, data=request.POST
            )
            if form.is_valid():
                form.save()
                return redirect(page)
            else:
                status = 400
        case "GET":
            form = WikiPageForm(workspace=page.workspace, instance=page)
            status = 200
        case _:
            raise RuntimeError("Shouldn't reach this")
    context = {"page": page, "form": form, "workspace": page.workspace}
    return render(
        request,
        "workspace/wiki_page_update.html",
        status=status,
        context=context,
    )
