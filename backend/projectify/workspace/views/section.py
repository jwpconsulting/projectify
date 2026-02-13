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

from rest_framework import serializers, status
from rest_framework.exceptions import NotFound
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from projectify.lib.error_schema import DeriveSchema
from projectify.lib.htmx import HttpResponseClientRedirect
from projectify.lib.schema import extend_schema
from projectify.lib.types import AuthenticatedHttpRequest
from projectify.lib.views import platform_view
from projectify.workspace.models import Section
from projectify.workspace.selectors.project import (
    ProjectDetailQuerySet,
    project_find_by_project_uuid,
)
from projectify.workspace.selectors.section import (
    SectionDetailQuerySet,
    section_find_for_user_and_uuid,
)
from projectify.workspace.serializers.section import SectionDetailSerializer
from projectify.workspace.services.section import (
    section_create,
    section_delete,
    section_minimize,
    section_move,
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


class SectionMinimizeForm(forms.Form):
    """Form for minimizing and expanding a section."""

    minimized = forms.BooleanField(required=False)


@platform_view
@require_POST
def section_minimize_view(
    request: AuthenticatedHttpRequest, section_uuid: UUID
) -> HttpResponse:
    """Toggle section minimize state."""
    section = section_find_for_user_and_uuid(
        user=request.user, section_uuid=section_uuid
    )
    if section is None:
        raise Http404(_("Section not found for this UUID"))

    form = SectionMinimizeForm(request.POST)
    if not form.is_valid():
        return HttpResponse("Invalid form data", status=400)

    minimized = form.cleaned_data["minimized"]
    section_minimize(who=request.user, section=section, minimized=minimized)
    return HttpResponseRedirect(section.get_absolute_url())


class SectionCreate(APIView):
    """Create a section."""

    class SectionCreateSerializer(serializers.ModelSerializer[Section]):
        """Parse section creation input."""

        project_uuid = serializers.UUIDField()

        class Meta:
            """Restrict fields to bare minimum needed for section creation."""

            model = Section
            fields = "title", "description", "project_uuid"

    @extend_schema(
        request=SectionCreateSerializer,
        responses={201: SectionDetailSerializer, 400: DeriveSchema},
    )
    def post(self, request: Request) -> Response:
        """Create a section."""
        user = request.user
        serializer = self.SectionCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        project_uuid: UUID = data["project_uuid"]
        project = project_find_by_project_uuid(
            project_uuid=project_uuid,
            who=request.user,
            archived=False,
        )
        if project is None:
            raise serializers.ValidationError(
                {"project_uuid": _("Could not find a project with this uuid")}
            )
        section = section_create(
            project=project,
            title=data["title"],
            description=data.get("description"),
            who=user,
        )
        output_serializer = SectionDetailSerializer(
            instance=section,
        )
        return Response(data=output_serializer.data, status=201)


# Read + Update + Delete
class SectionReadUpdateDelete(APIView):
    """Project retrieve view."""

    @extend_schema(
        responses={200: SectionDetailSerializer},
    )
    def get(self, request: Request, section_uuid: UUID) -> Response:
        """Handle GET."""
        section = section_find_for_user_and_uuid(
            user=request.user,
            section_uuid=section_uuid,
            qs=SectionDetailQuerySet,
        )
        if section is None:
            raise NotFound(_("Section not found for this UUID"))
        serializer = SectionDetailSerializer(instance=section)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    class SectionUpdateSerializer(serializers.ModelSerializer[Section]):
        """Input serializer for PUT."""

        class Meta:
            """Accept title and description."""

            fields = "title", "description"
            model = Section

    @extend_schema(
        request=SectionUpdateSerializer,
        responses={200: SectionUpdateSerializer, 400: DeriveSchema},
    )
    def put(self, request: Request, section_uuid: UUID) -> Response:
        """Update section."""
        section = section_find_for_user_and_uuid(
            user=request.user,
            section_uuid=section_uuid,
            qs=SectionDetailQuerySet,
        )
        if section is None:
            raise NotFound(_("Section not found for this UUID"))

        serializer = self.SectionUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        section_update(
            who=request.user,
            section=section,
            title=serializer.validated_data["title"],
            description=serializer.validated_data.get("description"),
        )
        return Response(data=serializer.validated_data)

    @extend_schema(
        responses={204: None},
    )
    def delete(self, request: Request, section_uuid: UUID) -> Response:
        """Handle DELETE."""
        section = section_find_for_user_and_uuid(
            user=request.user,
            section_uuid=section_uuid,
            qs=SectionDetailQuerySet,
        )
        if section is None:
            raise NotFound(_("Section not found for this UUID"))
        section_delete(
            who=self.request.user,
            section=section,
        )
        return Response(status=status.HTTP_204_NO_CONTENT)


# RPC
class SectionMove(APIView):
    """Insert a section at a given position."""

    class SectionMoveSerializer(serializers.Serializer):
        """Accept the desired position within project."""

        order = serializers.IntegerField()

    @extend_schema(
        request=SectionMoveSerializer,
        responses={200: None, 400: DeriveSchema},
    )
    def post(self, request: Request, section_uuid: UUID) -> Response:
        """Process request."""
        serializer = self.SectionMoveSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        user = request.user
        section = section_find_for_user_and_uuid(
            user=request.user,
            section_uuid=section_uuid,
            qs=SectionDetailQuerySet,
        )
        if section is None:
            raise NotFound(_("Section not found for this UUID"))
        section_move(
            section=section,
            order=data["order"],
            who=user,
        )
        section.refresh_from_db()
        return Response(status=status.HTTP_200_OK)
