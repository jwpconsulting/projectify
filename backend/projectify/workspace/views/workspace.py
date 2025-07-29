# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023, 2024 JWP Consulting GK
"""Workspace CRUD views."""

from typing import Any, TypedDict
from uuid import UUID

from django import forms
from django.http import Http404, HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_http_methods

from django_ratelimit.decorators import ratelimit
from rest_framework import parsers, serializers, views
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
)

from projectify.corporate.services.coupon import coupon_redeem
from projectify.corporate.services.customer import (
    customer_create_stripe_checkout_session,
)
from projectify.lib.error_schema import DeriveSchema
from projectify.lib.forms import populate_form_with_drf_errors
from projectify.lib.schema import extend_schema
from projectify.lib.types import AuthenticatedHttpRequest
from projectify.lib.views import platform_view

from ..exceptions import UserAlreadyAdded, UserAlreadyInvited
from ..models import Workspace
from ..selectors.project import project_find_by_workspace_uuid
from ..selectors.quota import workspace_get_all_quotas
from ..selectors.team_member import team_member_find_by_team_member_uuid
from ..selectors.workspace import (
    WorkspaceDetailQuerySet,
    workspace_build_detail_query_set,
    workspace_find_by_workspace_uuid,
    workspace_find_for_user,
)
from ..serializers.base import WorkspaceBaseSerializer
from ..serializers.workspace import WorkspaceDetailSerializer
from ..services.team_member import team_member_delete
from ..services.team_member_invite import (
    team_member_invite_create,
    team_member_invite_delete,
)
from ..services.workspace import workspace_create, workspace_update
from ..types import Quota


# HTML
@platform_view
def workspace_list_view(request: AuthenticatedHttpRequest) -> HttpResponse:
    """Show all workspaces."""
    workspaces = workspace_find_for_user(who=request.user)
    context = {"workspaces": workspaces}
    return render(request, "workspace/workspace_list.html", context)


@platform_view
def workspace_view(
    request: AuthenticatedHttpRequest, workspace_uuid: UUID
) -> HttpResponse:
    """Show workspace."""
    workspace = workspace_find_by_workspace_uuid(
        who=request.user, workspace_uuid=workspace_uuid
    )
    if workspace is None:
        raise Http404(_("Workspace not found"))
    projects = project_find_by_workspace_uuid(
        who=request.user,
        workspace_uuid=workspace_uuid,
        archived=False,
    )
    context = {"workspace": workspace, "projects": projects}
    return render(request, "workspace/workspace_detail.html", context)


class WorkspaceSettingsForm(forms.ModelForm):
    """Django form for workspace settings."""

    class Meta:
        """Meta."""

        fields = "title", "description", "picture"
        model = Workspace


@require_http_methods(["GET", "POST"])
@platform_view
def workspace_settings_general(
    request: AuthenticatedHttpRequest, workspace_uuid: UUID
) -> HttpResponse:
    """Show general workspace settings."""
    workspace = workspace_find_by_workspace_uuid(
        who=request.user, workspace_uuid=workspace_uuid
    )
    if workspace is None:
        raise Http404(_("Workspace not found"))
    if request.method == "GET":
        form = WorkspaceSettingsForm(instance=workspace)
        context = {"workspace": workspace, "form": form}
        return render(
            request,
            "workspace/workspace_settings_general.html",
            context=context,
        )
    form = WorkspaceSettingsForm(
        instance=workspace, data=request.POST, files=request.FILES
    )
    if not form.is_valid():
        context = {"workspace": workspace, "form": form}
        return render(
            request,
            "workspace/workspace_settings_general.html",
            context=context,
            status=400,
        )
    data = form.cleaned_data
    try:
        workspace_update(
            workspace=workspace,
            title=data["title"],
            description=data.get("description"),
            who=request.user,
            picture=data["picture"],
        )
    except ValidationError as error:
        populate_form_with_drf_errors(form, error)
        context = {"form": form}
        return render(
            request, "user/sign_up.html", context=context, status=400
        )
    return redirect(
        "dashboard:workspaces:settings",
        workspace.uuid,
    )


class InviteTeamMemberForm(forms.Form):
    """Form for inviting users."""

    email = forms.EmailField(
        label=_(
            "Enter the email address of the user you would like to invite"
        ),
        widget=forms.EmailInput(
            attrs={"placeholder": _("team-member@mail.com")}
        ),
    )

    class Meta:
        """Meta."""

        fields = "title", "description", "picture"
        model = Workspace


@require_http_methods(["GET"])
@platform_view
def workspace_settings_team_members(
    request: AuthenticatedHttpRequest, workspace_uuid: UUID
) -> HttpResponse:
    """Show team member settings."""
    # TODO add role change form
    workspace = workspace_find_by_workspace_uuid(
        who=request.user,
        workspace_uuid=workspace_uuid,
        qs=workspace_build_detail_query_set(who=request.user),
    )
    if workspace is None:
        raise Http404(_("Workspace not found"))
    context = {"workspace": workspace, "form": InviteTeamMemberForm()}
    return render(
        request,
        "workspace/workspace_settings_team_members.html",
        context=context,
    )


@require_http_methods(["POST"])
@platform_view
def workspace_settings_team_members_invite(
    request: AuthenticatedHttpRequest, workspace_uuid: UUID
) -> HttpResponse:
    """HTMX view to invite a team member."""
    workspace = workspace_find_by_workspace_uuid(
        who=request.user,
        workspace_uuid=workspace_uuid,
        qs=workspace_build_detail_query_set(who=request.user),
    )
    if workspace is None:
        raise Http404(_("Workspace not found"))

    form = InviteTeamMemberForm(request.POST)

    context = {"workspace": workspace, "form": form}
    if not form.is_valid():
        return render(
            request,
            "workspace/workspace_settings_team_members.html",
            context=context,
            status=400,
        )

    try:
        team_member_invite_create(
            who=request.user,
            workspace=workspace,
            email_or_user=form.cleaned_data["email"],
        )
    # TODO get rid of exceptions altogether
    except (UserAlreadyInvited, UserAlreadyAdded) as e:
        match e:
            case UserAlreadyInvited():
                form.add_error(
                    "email",
                    _("User has already been invited to this workspace."),
                )
            case UserAlreadyAdded():
                form.add_error(
                    "email",
                    _("User has already been added to this workspace."),
                )

        return render(
            request,
            "workspace/workspace_settings_team_members.html",
            context={"workspace": workspace, "form": form},
            status=400,
        )

    workspace.refresh_from_db()
    return render(
        request,
        "workspace/workspace_settings_team_members.html",
        context=context,
    )


@require_http_methods(["DELETE"])
@platform_view
def workspace_settings_team_member_remove(
    request: AuthenticatedHttpRequest,
    workspace_uuid: UUID,
    team_member_uuid: UUID,
) -> HttpResponse:
    """HTMX view to remove a team member."""
    workspace = workspace_find_by_workspace_uuid(
        who=request.user, workspace_uuid=workspace_uuid
    )
    if workspace is None:
        raise Http404(_("Workspace not found"))

    team_member = team_member_find_by_team_member_uuid(
        who=request.user, team_member_uuid=team_member_uuid
    )
    if team_member is None:
        raise Http404(_("Team member not found"))

    try:
        team_member_delete(team_member=team_member, who=request.user)
    except ValidationError as error:
        return HttpResponse(
            _("Failed to remove team member: {error}").format(
                error=str(error)
            ),
            status=400,
        )

    workspace.refresh_from_db()
    return render(
        request,
        "workspace/workspace_settings_team_members.html",
        context={"workspace": workspace, "form": InviteTeamMemberForm()},
    )


class UninviteTeamMemberForm(forms.Form):
    """Form for uninviting users."""

    email = forms.EmailField(widget=forms.HiddenInput())


@require_http_methods(["POST"])
@platform_view
def workspace_settings_team_member_uninvite(
    request: AuthenticatedHttpRequest, workspace_uuid: UUID
) -> HttpResponse:
    """HTMX view to uninvite a team member."""
    workspace = workspace_find_by_workspace_uuid(
        who=request.user,
        workspace_uuid=workspace_uuid,
        qs=workspace_build_detail_query_set(who=request.user),
    )
    if workspace is None:
        raise Http404(_("Workspace not found"))

    form = UninviteTeamMemberForm(request.POST)
    if not form.is_valid():
        return HttpResponse(_("Invalid form data"), status=400)

    try:
        team_member_invite_delete(
            workspace=workspace,
            who=request.user,
            email=form.cleaned_data["email"],
        )
    except ValidationError as error:
        return HttpResponse(
            _("Failed to uninvite team member: {error}").format(
                error=str(error)
            ),
            status=400,
        )

    workspace.refresh_from_db()
    context = {"workspace": workspace, "form": InviteTeamMemberForm()}
    return render(
        request,
        "workspace/workspace_settings_team_members.html",
        context=context,
    )


class WorkspaceBillingForm(forms.Form):
    """Django form for workspace billing actions."""

    action = forms.CharField(widget=forms.HiddenInput)
    seats = forms.IntegerField(
        min_value=1,
        max_value=100,
        required=False,
        widget=forms.NumberInput(
            attrs={"placeholder": _("Number of workspace seats")}
        ),
        label=_("Workspace seats"),
    )
    code = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={"placeholder": _("Enter coupon code")}),
        label=_("Coupon code"),
    )

    def clean(self) -> dict[str, Any]:
        """Make sure the right values are passed based on the action."""
        data = self.cleaned_data
        match data["action"]:
            case "redeem_coupon":
                if not data["code"]:
                    self.add_error("code", _("Must enter coupon code"))
            case "checkout":
                if not data["seats"]:
                    self.add_error("seats", _("Must enter number of seats"))

            case _:
                # XXX this error is not visible
                self.add_error(None, _("Invalid action selected"))
        return super().clean()


# XXX REFACTOR ME
PRICE_PER_SEAT = 8


@require_http_methods(["GET", "POST"])
@platform_view
def workspace_settings_billing(
    request: AuthenticatedHttpRequest, workspace_uuid: UUID
) -> HttpResponse:
    """Show workspace billing settings."""
    workspace = workspace_find_by_workspace_uuid(
        who=request.user, workspace_uuid=workspace_uuid
    )
    if workspace is None:
        raise Http404(_("Workspace not found"))
    workspace.quota = workspace_get_all_quotas(workspace)
    projects = project_find_by_workspace_uuid(
        who=request.user,
        workspace_uuid=workspace_uuid,
        archived=False,
    )

    context: dict[str, object] = {"workspace": workspace, "projects": projects}

    if request.method == "GET":
        match workspace.customer.subscription_status:
            case "UNPAID" | "CANCELLED":
                form = WorkspaceBillingForm()
                context = {**context, "form": form}
            case "ACTIVE":
                quota = workspace.quota.team_members_and_invites
                seats_remaining = (quota.limit or 0) - (quota.current or 0)
                context = {
                    **context,
                    "monthly_total": workspace.customer.seats * PRICE_PER_SEAT,
                    "seats_remaining": seats_remaining,
                    "price_per_seat": PRICE_PER_SEAT,
                }
            case "CUSTOM":
                pass
            case other:
                raise ValueError(f"Unexpected subscription_status {other}")

        return render(
            request,
            "workspace/workspace_settings_billing.html",
            context=context,
        )
    form = WorkspaceBillingForm(request.POST)

    match workspace.customer.subscription_status:
        case "UNPAID" | "CANCELLED":
            pass
        case _:
            return HttpResponseBadRequest(
                _(
                    "You've already activated a subscription for this workspace"
                ),
            )
    context = {**context, "form": form}
    if not form.is_valid():
        return render(
            request,
            "workspace/workspace_settings_billing.html",
            context=context,
        )
    data = form.cleaned_data
    # Checkout session
    match data["action"]:
        case "checkout":
            try:
                session = customer_create_stripe_checkout_session(
                    customer=workspace.customer,
                    who=request.user,
                    seats=data["seats"],
                )
            except ValidationError as e:
                populate_form_with_drf_errors(form, e)
                return render(
                    request,
                    "workspace/workspace_settings_billing.html",
                    context=context,
                )
            return redirect(session.url)
        case "redeem_coupon":
            try:
                coupon_redeem(
                    who=request.user, code=data["code"], workspace=workspace
                )
            except ValidationError as e:
                populate_form_with_drf_errors(form, e)
                return render(
                    request,
                    "workspace/workspace_settings_billing.html",
                    context=context,
                )
            return redirect("dashboard:workspaces:billing", workspace.uuid)
        case _:
            return HttpResponseBadRequest()


QuotaEntry = TypedDict("QuotaEntry", {"label": str, "quota": Quota})


@platform_view
def workspace_settings_quota(
    request: AuthenticatedHttpRequest, workspace_uuid: UUID
) -> HttpResponse:
    """Show workspace quota."""
    workspace = workspace_find_by_workspace_uuid(
        who=request.user, workspace_uuid=workspace_uuid
    )
    if workspace is None:
        raise Http404(_("Workspace not found"))
    workspace.quota = workspace_get_all_quotas(workspace)
    projects = project_find_by_workspace_uuid(
        who=request.user,
        workspace_uuid=workspace_uuid,
        archived=False,
    )

    quota_rows: list[QuotaEntry] = [
        {
            "label": _("Team members and invites"),
            "quota": workspace.quota.team_members_and_invites,
        },
        {
            "label": _("Projects"),
            "quota": workspace.quota.projects,
        },
        {
            "label": _("Sections"),
            "quota": workspace.quota.sections,
        },
        {
            "label": _("Tasks"),
            "quota": workspace.quota.tasks,
        },
        {
            "label": _("Labels"),
            "quota": workspace.quota.labels,
        },
        {
            "label": _("Sub tasks"),
            "quota": workspace.quota.sub_tasks,
        },
        {
            "label": _("Task labels"),
            "quota": workspace.quota.task_labels,
        },
    ]
    quota_rows = [q for q in quota_rows if q["quota"].limit is not None]

    context = {
        "workspace": workspace,
        "quota_rows": quota_rows,
        "projects": projects,
    }
    return render(
        request, "workspace/workspace_settings_quota.html", context=context
    )


# Create
class WorkspaceCreate(views.APIView):
    """Create a workspace."""

    class WorkspaceCreateSerializer(serializers.ModelSerializer[Workspace]):
        """Accept title, description."""

        class Meta:
            """Meta."""

            fields = "title", "description"
            model = Workspace

    @extend_schema(
        request=WorkspaceCreateSerializer,
        responses={201: WorkspaceBaseSerializer, 400: DeriveSchema},
    )
    def post(self, request: Request) -> Response:
        """Create the workspace and add this user."""
        serializer = self.WorkspaceCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        workspace = workspace_create(
            title=serializer.validated_data["title"],
            description=serializer.validated_data.get("description"),
            owner=self.request.user,
        )
        result = WorkspaceBaseSerializer(instance=workspace)
        return Response(status=HTTP_201_CREATED, data=result.data)


# Read
class UserWorkspaces(views.APIView):
    """List all workspaces for a user."""

    class UserWorkspaceSerializer(serializers.ModelSerializer[Workspace]):
        """Serialize a workspace for overview purposes."""

        class Meta:
            """Return only the bare minimum."""

            fields = ("title", "uuid")
            model = Workspace

    @extend_schema(responses={200: UserWorkspaceSerializer(many=True)})
    def get(self, request: Request) -> Response:
        """Handle GET."""
        workspaces = workspace_find_for_user(who=request.user)
        serializer = self.UserWorkspaceSerializer(
            instance=workspaces, many=True
        )
        return Response(status=HTTP_200_OK, data=serializer.data)


# Read + Update
class WorkspaceReadUpdate(views.APIView):
    """Workspace read and update view."""

    @extend_schema(
        responses={200: WorkspaceDetailSerializer},
    )
    def get(self, request: Request, workspace_uuid: UUID) -> Response:
        """Handle GET."""
        workspace = workspace_find_by_workspace_uuid(
            who=request.user,
            workspace_uuid=workspace_uuid,
            qs=WorkspaceDetailQuerySet,
        )
        if workspace is None:
            raise NotFound(_("Could not find workspace with this UUID"))
        workspace.quota = workspace_get_all_quotas(workspace)
        serializer = WorkspaceDetailSerializer(instance=workspace)
        return Response(status=HTTP_200_OK, data=serializer.data)

    class WorkspaceUpdateSerializer(serializers.ModelSerializer[Workspace]):
        """Accept title, description."""

        class Meta:
            """Meta."""

            fields = "title", "description"
            model = Workspace

    @extend_schema(
        request=WorkspaceUpdateSerializer,
        responses={200: WorkspaceUpdateSerializer, 400: DeriveSchema},
    )
    def put(self, request: Request, workspace_uuid: UUID) -> Response:
        """Handle PUT."""
        workspace = workspace_find_by_workspace_uuid(
            who=request.user,
            workspace_uuid=workspace_uuid,
            qs=WorkspaceDetailQuerySet,
        )
        if workspace is None:
            raise NotFound(_("Could not find workspace with this UUID"))

        serializer = self.WorkspaceUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        workspace_update(
            workspace=workspace,
            title=serializer.validated_data["title"],
            description=serializer.validated_data.get("description"),
            who=self.request.user,
            picture=None,
        )
        return Response(status=HTTP_200_OK, data=serializer.data)


# Delete


# RPC
class WorkspacePictureUploadView(views.APIView):
    """View that allows uploading a profile picture."""

    parser_classes = (parsers.MultiPartParser,)

    class WorkspacePictureUploadSerializer(serializers.Serializer):
        """Deserialize an image attachment."""

        file = serializers.ImageField(required=False)

    @extend_schema(
        request=WorkspacePictureUploadSerializer,
        responses={204: None, 400: DeriveSchema},
    )
    def post(self, request: Request, workspace_uuid: UUID) -> Response:
        """Handle POST."""
        workspace = workspace_find_by_workspace_uuid(
            who=request.user, workspace_uuid=workspace_uuid
        )
        if workspace is None:
            raise NotFound(
                _("Could not find workspace with UUID for picture upload")
            )

        serializer = self.WorkspacePictureUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        file_obj = serializer.validated_data.get("file")
        if file_obj is None:
            workspace.picture.delete()
        else:
            workspace.picture = file_obj
        workspace.save()
        return Response(status=204)


class InviteUserToWorkspace(views.APIView):
    """Invite a user to a workspace."""

    class InviteUserToWorkspaceSerializer(serializers.Serializer):
        """Accept email."""

        email = serializers.EmailField()

    @extend_schema(
        request=InviteUserToWorkspaceSerializer,
        responses={201: InviteUserToWorkspaceSerializer, 400: DeriveSchema},
    )
    @method_decorator(ratelimit(key="user", rate="5/h"))
    def post(self, request: Request, workspace_uuid: UUID) -> Response:
        """Handle POST."""
        workspace = workspace_find_by_workspace_uuid(
            workspace_uuid=workspace_uuid, who=request.user
        )
        if workspace is None:
            raise NotFound(_("No workspace found for this UUID"))

        serializer = self.InviteUserToWorkspaceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email: str = serializer.validated_data["email"]
        try:
            team_member_invite_create(
                who=request.user, workspace=workspace, email_or_user=email
            )
        except UserAlreadyInvited:
            raise serializers.ValidationError(
                {
                    "email": _(
                        "User with email {email} has already been invited to "
                        "this workspace."
                    ).format(email=email)
                }
            )
        except UserAlreadyAdded:
            raise serializers.ValidationError(
                {
                    "email": _(
                        "User with email {email} has already been added to "
                        "this workspace."
                    ).format(email=email)
                }
            )
        return Response(data=serializer.data, status=HTTP_201_CREATED)


class UninviteUserFromWorkspace(views.APIView):
    """Remove a user invitation."""

    class UninviteUserFromWorkspaceSerializer(serializers.Serializer):
        """Accept email."""

        email = serializers.EmailField()

    @extend_schema(
        request=UninviteUserFromWorkspaceSerializer,
        responses={204: None, 400: DeriveSchema},
    )
    def post(self, request: Request, workspace_uuid: UUID) -> Response:
        """Handle POST."""
        workspace = workspace_find_by_workspace_uuid(
            workspace_uuid=workspace_uuid, who=request.user
        )
        if workspace is None:
            raise NotFound(_("No workspace found for this UUID"))
        serializer = self.UninviteUserFromWorkspaceSerializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        team_member_invite_delete(
            workspace=workspace,
            who=request.user,
            email=serializer.validated_data["email"],
        )
        return Response(data=serializer.data, status=HTTP_204_NO_CONTENT)
