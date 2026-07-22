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

from projectify.lib.types import AuthenticatedHttpRequest
from projectify.lib.views import platform_view
from projectify.workspace.forms import WorkspaceRichTextEditor

from ..models import WikiPage, Workspace
from ..selectors.wiki import (
    WikiPageDetailQuerySet,
    wiki_find_by_workspace_and_page_title,
    wiki_find_recent_changes,
)
from ..selectors.workspace import (
    WorkspaceDetailQuerySet,
    workspace_find_by_workspace_uuid,
)
from ..services.wiki import wiki_page_get_or_create_index

logger = logging.getLogger(__name__)


@platform_view
@require_GET
def wiki_recent_changes(
    request: AuthenticatedHttpRequest, ws_uuid: UUID
) -> HttpResponse:
    """Show recently changed wiki pages."""
    ws = workspace_find_by_workspace_uuid(
        who=request.user, workspace_uuid=ws_uuid, qs=WorkspaceDetailQuerySet
    )
    if ws is None:
        raise Http404(_("Workspace not found"))
    pages = wiki_find_recent_changes(who=request.user, workspace=ws)
    context = {
        "workspace": ws,
        "projects": ws.project_set.all(),
        "pages": pages,
    }
    return render(
        request, "workspace/wiki_recent_changes.html", context=context
    )


@platform_view
@require_GET
def wiki_index(
    request: AuthenticatedHttpRequest, ws_uuid: UUID
) -> HttpResponse:
    """Return the default Wiki index page."""
    ws = workspace_find_by_workspace_uuid(
        who=request.user, workspace_uuid=ws_uuid, qs=WorkspaceDetailQuerySet
    )
    if ws is None:
        raise Http404(_("Workspace not found"))
    page = wiki_page_get_or_create_index(workspace=ws, who=request.user)
    context = {
        "page": page,
        "workspace": page.workspace,
        "projects": page.workspace.project_set.all(),
    }
    return render(request, "workspace/wiki_page_detail.html", context=context)


class WikiPageForm(forms.ModelForm):
    """Form for WikiPage."""

    def __init__(self, *args: Any, workspace: Workspace, **kwargs: Any):
        """Populate available assignees and optionally set autofocus."""
        match kwargs:
            case {"instance": WikiPage() as instance}:
                self.page_title = instance.title
            case {"page_title": str()}:
                self.page_title = kwargs.pop("page_title")
            case other:
                raise ValueError(
                    f"Must call with page_title, received {other}"
                )
        super().__init__(*args, **kwargs)
        self.workspace = workspace
        self.fields["content"].widget = WorkspaceRichTextEditor(self.workspace)

    def save(self, *args: Any, **kwargs: Any) -> WikiPage:
        """Set workspace, title before saving."""
        self.instance.workspace = self.workspace
        self.instance.title = self.page_title
        result: WikiPage = super().save(*args, **kwargs)
        return result

    class Meta:
        """Meta."""

        model = WikiPage
        fields = ("content",)


@platform_view
@require_GET
def wiki_page_view(
    request: AuthenticatedHttpRequest, ws_uuid: UUID, page_title: str
) -> HttpResponse:
    """Upload an image attachment to a workspace."""
    page = wiki_find_by_workspace_and_page_title(
        ws_uuid=ws_uuid,
        who=request.user,
        title=page_title,
        qs=WikiPageDetailQuerySet,
    )
    if page is None:
        ws = workspace_find_by_workspace_uuid(
            who=request.user,
            workspace_uuid=ws_uuid,
            qs=WorkspaceDetailQuerySet,
        )
        if ws is None:
            raise Http404(_("Workspace not found"))
        return redirect(
            reverse("dashboard:wiki:edit", args=(ws_uuid, page_title))
        )
    context = {
        "page": page,
        "workspace": page.workspace,
        # XXX slow
        "projects": page.workspace.project_set.all(),
    }
    return render(request, "workspace/wiki_page_detail.html", context=context)


@platform_view
@require_http_methods(["GET", "POST"])
def wiki_page_edit(
    request: AuthenticatedHttpRequest, ws_uuid: UUID, page_title: str
) -> HttpResponse:
    """Upload an image attachment to a workspace."""
    page = wiki_find_by_workspace_and_page_title(
        ws_uuid=ws_uuid,
        who=request.user,
        title=page_title,
        qs=WikiPageDetailQuerySet,
    )
    if page is None:
        ws = workspace_find_by_workspace_uuid(
            who=request.user,
            workspace_uuid=ws_uuid,
            qs=WorkspaceDetailQuerySet,
        )
        if ws is None:
            raise Http404(_("Workspace not found"))
        match request.method:
            case "POST":
                form = WikiPageForm(
                    workspace=ws, page_title=page_title, data=request.POST
                )
                if form.is_valid():
                    page = form.save()
                    return redirect(page)
                else:
                    status = 400
            case "GET":
                form = WikiPageForm(workspace=ws, page_title=page_title)
                status = 200
            case _:
                raise RuntimeError("Shouldn't reach this")
        context: dict[str, Any] = {
            "form": form,
            "workspace": ws,
            "projects": ws.project_set.all(),
            "page_title": page_title,
        }
    else:
        ws = page.workspace
        match request.method:
            case "POST":
                form = WikiPageForm(
                    workspace=ws, instance=page, data=request.POST
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
    context = {
        "page": page,
        "form": form,
        "workspace": ws,
        # XXX slow
        "projects": ws.project_set.all(),
    }
    return render(
        request,
        "workspace/wiki_page_update.html",
        status=status,
        context=context,
    )
