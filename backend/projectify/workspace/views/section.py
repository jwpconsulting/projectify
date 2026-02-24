# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023-2026 JWP Consulting GK
"""Section views."""

from typing import Any, Optional
from uuid import UUID

from django import forms
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_POST

from projectify.lib.htmx import HttpResponseClientRedirect
from projectify.lib.types import AuthenticatedHttpRequest
from projectify.lib.views import platform_view
from projectify.workspace.selectors.project import (
    ProjectDetailQuerySet,
    project_find_by_project_uuid,
)
from projectify.workspace.selectors.section import (
    SectionDetailQuerySet,
    section_find_for_user_and_uuid,
)
from projectify.workspace.services.section import (
    section_create,
    section_delete,
    section_move_in_direction,
    section_update,
)


class SectionCreateForm(forms.Form):
    """Form for updating section."""

    title = forms.CharField(
        max_length=255,
        widget=forms.TextInput(),
    )
    description = forms.CharField(
        required=False,
        widget=forms.Textarea(),
    )


@platform_view
def section_create_view(
    request: AuthenticatedHttpRequest, project_uuid: UUID
) -> HttpResponse:
    """Update section view."""
    project = project_find_by_project_uuid(
        who=request.user, project_uuid=project_uuid, qs=ProjectDetailQuerySet
    )
    if project is None:
        raise Http404(_("Project not found for this UUID"))

    context: dict[str, Any] = {
        "project": project,
        "workspace": project.workspace,
        "projects": project.workspace.project_set.all(),
    }

    if request.method == "GET":
        form = SectionCreateForm()
        context = {**context, "form": form}
        return render(request, "workspace/section_create.html", context)

    form = SectionCreateForm(request.POST)
    if not form.is_valid():
        context = {"form": form, **context}
        return render(
            request, "workspace/section_create.html", context, status=400
        )
    section = section_create(
        who=request.user,
        project=project,
        title=form.cleaned_data["title"],
        description=form.cleaned_data.get("description") or None,
    )

    return redirect(section.get_absolute_url())


@platform_view
def section_detail(
    request: AuthenticatedHttpRequest, section_uuid: UUID
) -> HttpResponse:
    """Redirect to project with this section visible."""
    section = section_find_for_user_and_uuid(
        user=request.user, section_uuid=section_uuid
    )
    if section is None:
        raise Http404(_("Section not found for this UUID"))
    return redirect(section.get_absolute_url())


class SectionUpdateForm(forms.Form):
    """Form for updating section."""

    title = forms.CharField(
        max_length=255,
        widget=forms.TextInput(),
    )
    description = forms.CharField(
        required=False,
        widget=forms.Textarea(),
    )


@platform_view
def section_update_view(
    request: AuthenticatedHttpRequest, section_uuid: UUID
) -> HttpResponse:
    """Update section view."""
    section = section_find_for_user_and_uuid(
        user=request.user, section_uuid=section_uuid, qs=SectionDetailQuerySet
    )
    if section is None:
        raise Http404(_("Section not found for this UUID"))

    context: dict[str, Any] = {
        "section": section,
        "project": section.project,
        "projects": section.project.workspace.project_set.all(),
        "workspace": section.project.workspace,
    }

    if request.method == "GET":
        form = SectionUpdateForm(
            initial={
                "title": section.title,
                "description": section.description,
            }
        )

        context = {"form": form, **context}
        return render(request, "workspace/section_update.html", context)

    action: Optional[str] = request.POST.get("action")

    match action:
        case "save":
            form = SectionUpdateForm(request.POST)
            if not form.is_valid():
                context = {"form": form, **context}
                return render(
                    request,
                    "workspace/section_update.html",
                    context,
                    status=400,
                )
            section_update(
                who=request.user,
                section=section,
                title=form.cleaned_data["title"],
                description=form.cleaned_data.get("description") or None,
            )
        case "move_up":
            section_move_in_direction(
                section=section, direction="up", who=request.user
            )
        case "move_down":
            section_move_in_direction(
                section=section, direction="down", who=request.user
            )
        case _:
            return HttpResponse("Invalid action", status=400)
    return HttpResponseRedirect(section.get_absolute_url())


@platform_view
@require_POST
def section_delete_view(
    request: AuthenticatedHttpRequest, section_uuid: UUID
) -> HttpResponse:
    """Update section view."""
    section = section_find_for_user_and_uuid(
        user=request.user, section_uuid=section_uuid
    )
    if section is None:
        raise Http404(_("Section not found for this UUID"))

    project_url = reverse(
        "dashboard:projects:detail", args=(section.project.uuid,)
    )
    section_delete(who=request.user, section=section)
    return HttpResponseClientRedirect(project_url)
