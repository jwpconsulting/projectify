# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023-2026 JWP Consulting GK
"""Workspace CRUD views."""

import logging
from dataclasses import dataclass
from typing import Any, TypedDict
from uuid import UUID

from django import forms
from django.core import exceptions
from django.db.models import QuerySet
from django.http import Http404, HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_http_methods

from rest_framework import serializers

from projectify.corporate.selectors.customer import (
    customer_find_by_workspace_uuid,
)
from projectify.corporate.services.coupon import coupon_redeem
from projectify.corporate.services.customer import (
    create_billing_portal_session_for_customer,
    customer_create_stripe_checkout_session,
)
from projectify.lib.forms import populate_form_with_drf_errors
from projectify.lib.htmx import HttpResponseClientRefresh
from projectify.lib.types import AuthenticatedHttpRequest
from projectify.lib.views import platform_view

from ..models import Label, TeamMember, Workspace
from ..models.const import COLOR_MAP
from ..selectors.labels import (
    LabelDetailQuerySet,
    label_find_by_label_uuid,
    labels_annotate_with_colors,
)
from ..selectors.project import project_find_by_workspace_uuid
from ..selectors.quota import workspace_get_all_quotas
from ..selectors.team_member import (
    team_member_find_by_team_member_uuid,
    team_member_find_for_workspace,
    team_member_last_project_for_user,
)
from ..selectors.workspace import (
    WorkspaceDetailQuerySet,
    workspace_build_detail_query_set,
    workspace_find_by_workspace_uuid,
    workspace_find_for_user,
)
from ..services.label import label_create, label_delete, label_update
from ..services.team_member import (
    team_member_delete,
    team_member_minimize_project_list,
    team_member_update,
    team_member_visit_workspace,
)
from ..services.team_member_invite import (
    team_member_invite_create,
    team_member_invite_delete,
)
from ..services.workspace import workspace_update
from ..types import Quota

logger = logging.getLogger(__name__)


@dataclass(kw_only=True, frozen=True)
class ColorInfo:
    """Color information for form widgets."""

    name: str
    bg_class: str
    border_class: str
    text_class: str


def create_color_choices() -> dict[Any, ColorInfo]:
    """Create color choices for label colors."""
    return {
        i: ColorInfo(
            name=info["name"],
            bg_class=info["bg_class"],
            border_class=info["border_class"],
            text_class=info["text_class"],
        )
        for i, info in COLOR_MAP.items()
    }


def _get_workspace_settings_context(
    request: AuthenticatedHttpRequest,
    workspace: Workspace,
    active_tab: str,
) -> dict[str, object]:
    """Get shared context for workspace settings views."""
    return {
        "workspace": workspace,
        "projects": workspace.project_set.all(),
        "workspaces": workspace_find_for_user(who=request.user),
        "current_team_member_qs": team_member_find_for_workspace(
            user=request.user, workspace=workspace
        ),
        "active_tab": active_tab,
    }


# HTML
@platform_view
def workspace_view(
    request: AuthenticatedHttpRequest, workspace_uuid: UUID
) -> HttpResponse:
    """Show workspace."""
    workspace = workspace_find_by_workspace_uuid(
        who=request.user,
        workspace_uuid=workspace_uuid,
        qs=WorkspaceDetailQuerySet,
    )
    if workspace is None:
        raise Http404(_("Workspace not found"))

    # Mark this workspace as most recently visited
    team_member = team_member_find_for_workspace(
        user=request.user, workspace=workspace
    )
    if team_member is None:
        raise Http404(_("Team member not found"))
    team_member_visit_workspace(team_member=team_member)

    # Check whether the user has already visited a project within this
    # workspace
    last_project = team_member_last_project_for_user(
        user=request.user, workspace=workspace
    )
    if last_project:
        return redirect(last_project.get_absolute_url())

    project = workspace.project_set.first()
    if project:
        return redirect(project.get_absolute_url())
    return redirect("onboarding:new_project", workspace_uuid=workspace_uuid)


class MinimizeProjectListForm(forms.Form):
    """Form for minimizingand expanding the project list."""

    minimized = forms.BooleanField(required=False)

    def __init__(self, workspace: Workspace, *args: Any, **kwargs: Any):
        """Create current project field."""
        super().__init__(*args, **kwargs)
        self.fields["current_project"] = forms.ModelChoiceField(
            required=False,
            to_field_name="uuid",
            # Hopefully this project_set only contains non-archived projects
            queryset=workspace.project_set.all(),
        )


@require_http_methods(["POST"])
@platform_view
def workspace_minimize_project_list(
    request: AuthenticatedHttpRequest, workspace_uuid: UUID
) -> HttpResponse:
    """Toggle the minimized state of the project list."""
    assert request.method == "POST"
    workspace = workspace_find_by_workspace_uuid(
        workspace_uuid=workspace_uuid,
        who=request.user,
        qs=WorkspaceDetailQuerySet,
    )
    if workspace is None:
        raise Http404(_("No workspace found for this UUID"))

    form = MinimizeProjectListForm(workspace, request.POST)
    if not form.is_valid():
        return HttpResponse(status=400)

    current_team_member_qs = team_member_find_for_workspace(
        user=request.user, workspace=workspace
    )
    if current_team_member_qs is None:
        raise Http404(_("Team member not found"))

    team_member_minimize_project_list(
        team_member=current_team_member_qs,
        minimized=form.cleaned_data["minimized"],
    )

    context = {
        "workspace": workspace,
        "project": form.cleaned_data.get("current_project"),
        "projects": workspace.project_set.all(),
        "current_team_member_qs": current_team_member_qs,
    }

    return render(
        request,
        "workspace/common/sidemenu/project_details.html",
        context=context,
    )


class WorkspaceSettingsForm(forms.ModelForm):
    """Django form for workspace settings."""

    class Meta:
        """Meta."""

        fields = "picture", "title", "description"
        model = Workspace
        labels = {
            "picture": _("Workspace picture"),
        }
        widgets = {
            "picture": forms.ClearableFileInput(
                attrs={
                    "initial_text": _("No picture uploaded"),
                    "clear_checkbox_label": _("Remove workspace picture"),
                    "cleared": _("You haven't uploaded a workspace picture"),
                }
            ),
        }


@require_http_methods(["GET", "POST"])
@platform_view
def workspace_settings_general(
    request: AuthenticatedHttpRequest, workspace_uuid: UUID
) -> HttpResponse:
    """Show general workspace settings."""
    workspace = workspace_find_by_workspace_uuid(
        who=request.user,
        workspace_uuid=workspace_uuid,
        qs=WorkspaceDetailQuerySet,
    )
    if workspace is None:
        raise Http404(_("Workspace not found"))
    context = _get_workspace_settings_context(
        request=request, workspace=workspace, active_tab="general"
    )
    if request.method == "GET":
        form = WorkspaceSettingsForm(instance=workspace)
        context = {**context, "form": form}
        return render(
            request,
            "workspace/workspace_settings_general.html",
            context=context,
        )
    form = WorkspaceSettingsForm(
        instance=workspace, data=request.POST, files=request.FILES
    )
    if not form.is_valid():
        context = {**context, "form": form}
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
    except serializers.ValidationError as error:
        populate_form_with_drf_errors(form, error)
        context = {**context, "form": form}
        return render(
            request,
            "workspace/workspace_settings_general.html",
            context=context,
            status=400,
        )
    return redirect(
        "dashboard:workspaces:settings",
        workspace.uuid,
    )


@require_http_methods(["GET"])
@platform_view
def workspace_settings_projects(
    request: AuthenticatedHttpRequest, workspace_uuid: UUID
) -> HttpResponse:
    """Show projects for this workspace."""
    workspace = workspace_find_by_workspace_uuid(
        who=request.user,
        workspace_uuid=workspace_uuid,
        qs=WorkspaceDetailQuerySet,
    )
    if workspace is None:
        raise Http404(_("Workspace not found"))
    context = _get_workspace_settings_context(
        request=request, workspace=workspace, active_tab="projects"
    )
    archived_projects = project_find_by_workspace_uuid(
        workspace_uuid=workspace_uuid,
        who=request.user,
        archived=True,
    )
    context["archived_projects"] = archived_projects
    return render(
        request,
        "workspace/workspace_settings_projects.html",
        context=context,
    )


@require_http_methods(["GET"])
@platform_view
def workspace_settings_label(
    request: AuthenticatedHttpRequest, workspace_uuid: UUID
) -> HttpResponse:
    """Show labels for this workspace."""
    workspace = workspace_find_by_workspace_uuid(
        who=request.user,
        workspace_uuid=workspace_uuid,
        qs=workspace_build_detail_query_set(
            who=None,
            annotate_labels=True,
        ),
    )
    if workspace is None:
        raise Http404(_("Workspace not found"))
    context = {
        **_get_workspace_settings_context(
            request=request, workspace=workspace, active_tab="labels"
        ),
        "labels": labels_annotate_with_colors(workspace.label_set.all()),
    }
    return render(
        request, "workspace/workspace_settings_labels.html", context=context
    )


class LabelCreateForm(forms.ModelForm):
    """Form for creating labels."""

    name = forms.CharField(max_length=100)
    color = forms.IntegerField()

    def __init__(self, *args: Any, **kwargs: Any):
        """Initialize form with color widget."""
        super().__init__(*args, **kwargs)
        color_widget = forms.RadioSelect()
        color_widget.option_template_name = (
            "workspace/forms/widgets/select_label_option.html"
        )

        self.fields["color"] = forms.ChoiceField(
            label=_("Color"),
            choices=create_color_choices(),
            widget=color_widget,
        )

    class Meta:
        """Meta settings for LabelCreateForm."""

        fields = "name", "color"
        model = Label


@require_http_methods(["GET", "POST"])
@platform_view
def workspace_settings_new_label(
    request: AuthenticatedHttpRequest, workspace_uuid: UUID
) -> HttpResponse:
    """Create a new label for the workspace."""
    workspace = workspace_find_by_workspace_uuid(
        who=request.user,
        workspace_uuid=workspace_uuid,
        qs=WorkspaceDetailQuerySet,
    )
    if workspace is None:
        raise Http404(_("Workspace not found"))

    context = {
        **_get_workspace_settings_context(
            request=request, workspace=workspace, active_tab="labels"
        ),
        "color_map": COLOR_MAP,
    }
    match request.method:
        case "GET":
            form = LabelCreateForm()
            return render(
                request,
                "workspace/workspace_settings_create_label.html",
                context={**context, "form": form},
            )
        case "POST":
            pass
        case other:
            raise ValueError(f"Wrong HTTP method {other}")
    form = LabelCreateForm(data=request.POST)
    if not form.is_valid():
        return render(
            request,
            "workspace/workspace_settings_create_label.html",
            context={**context, "form": form},
            status=400,
        )

    try:
        label_create(
            workspace=workspace,
            name=form.cleaned_data["name"],
            color=form.cleaned_data["color"],
            who=request.user,
        )
    except (exceptions.ValidationError, serializers.ValidationError) as error:
        populate_form_with_drf_errors(form, error)
        return render(
            request,
            "workspace/workspace_settings_create_label.html",
            context={**context, "form": form},
            status=400,
        )

    return redirect("dashboard:workspaces:labels", workspace.uuid)


class LabelUpdateForm(forms.ModelForm):
    """Form for updating labels."""

    name = forms.CharField()
    color = forms.IntegerField()

    def __init__(self, labels: QuerySet[Label], *args: Any, **kwargs: Any):
        """Initialize form with color widget."""
        super().__init__(*args, **kwargs)
        color_widget = forms.RadioSelect()
        color_widget.option_template_name = (
            "workspace/forms/widgets/select_label_option.html"
        )

        self.fields["color"] = forms.ChoiceField(
            label=_("Color"),
            choices=create_color_choices(),
            widget=color_widget,
        )

    class Meta:
        """Meta settings for LabelUpdateForm."""

        fields = "name", "color"
        model = Label


@require_http_methods(["GET", "POST", "DELETE"])
@platform_view
def workspace_settings_edit_label(
    request: AuthenticatedHttpRequest, workspace_uuid: UUID, label_uuid: UUID
) -> HttpResponse:
    """Show edit view for specific label."""
    label = label_find_by_label_uuid(
        who=request.user,
        label_uuid=label_uuid,
        qs=LabelDetailQuerySet,
    )
    if label is None:
        raise Http404(f"Couldn't find label with UUID {label_uuid}")
    if label.workspace.uuid != workspace_uuid:
        return HttpResponseBadRequest("Workspace UUIDs don't match")
    context = {
        **_get_workspace_settings_context(
            request=request, workspace=label.workspace, active_tab="labels"
        ),
        "label": label,
        "color_map": COLOR_MAP,
    }
    match request.method:
        case "DELETE":
            label_delete(who=request.user, label=label)
            return HttpResponseClientRefresh()
        case "GET":
            form = LabelUpdateForm(
                labels=label.workspace.label_set.all(), instance=label
            )
            return render(
                request,
                "workspace/workspace_settings_edit_label.html",
                context={**context, "form": form},
            )
        case "POST":
            pass
        case other:
            raise ValueError(f"Wrong HTTP method {other}")
    form = LabelUpdateForm(
        labels=label.workspace.label_set.all(),
        instance=label,
        data=request.POST,
    )
    if not form.is_valid():
        return render(
            request,
            "workspace/workspace_settings_edit_label.html",
            context={**context, "form": form},
            status=400,
        )
    try:
        label_update(
            who=request.user,
            label=label,
            name=form.cleaned_data["name"],
            color=form.cleaned_data["color"],
        )
    except (exceptions.ValidationError, serializers.ValidationError) as error:
        populate_form_with_drf_errors(form, error)
        return render(
            request,
            "workspace/workspace_settings_edit_label.html",
            context={**context, "form": form},
            status=400,
        )
    return redirect("dashboard:workspaces:labels", label.workspace.uuid)


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


class UninviteTeamMemberForm(forms.Form):
    """Form for uninviting users."""

    email = forms.EmailField(widget=forms.HiddenInput())


class RemoveTeamMemberForm(forms.Form):
    """Form for removing team members."""

    def __init__(self, workspace: Workspace, *args: Any, **kwargs: Any):
        """Initialize form with workspace team members."""
        super().__init__(*args, **kwargs)
        self.fields["team_member"] = forms.ModelChoiceField(
            to_field_name="uuid",
            widget=forms.HiddenInput(),
            queryset=workspace.teammember_set.all(),
        )


@require_http_methods(["GET", "POST"])
@platform_view
def workspace_settings_team_members(
    request: AuthenticatedHttpRequest, workspace_uuid: UUID
) -> HttpResponse:
    """Show team member settings and handle role changes."""
    workspace_qs = workspace_build_detail_query_set(who=None)
    workspace = workspace_find_by_workspace_uuid(
        who=request.user, workspace_uuid=workspace_uuid, qs=workspace_qs
    )
    if workspace is None:
        raise Http404(_("Workspace not found"))
    template = "workspace/workspace_settings_team_members.html"

    additional_context = {}
    match request.method, request.POST.get("action"):
        case "POST", "invite":
            invite_form = InviteTeamMemberForm(request.POST)
            additional_context = {"invite_form": invite_form}
            if invite_form.is_valid():
                try:
                    team_member_invite_create(
                        who=request.user,
                        workspace=workspace,
                        email_or_user=invite_form.cleaned_data["email"],
                    )
                    status = 200
                except serializers.ValidationError as e:
                    populate_form_with_drf_errors(invite_form, e)
                    status = 400
            else:
                status = 400
        case "POST", "uninvite":
            # I thought about adding aformset for editing the team
            # members and invites. I've decided that I can always do that later
            # Justus 2026-02-28
            uninvite_form = UninviteTeamMemberForm(request.POST)
            if not uninvite_form.is_valid():
                return HttpResponse(_("Invalid form data"), status=400)
            try:
                team_member_invite_delete(
                    workspace=workspace,
                    who=request.user,
                    email=uninvite_form.cleaned_data["email"],
                )
            except serializers.ValidationError as error:
                return HttpResponse(
                    _("Failed to uninvite team member: {error}").format(
                        error=str(error)
                    ),
                    status=400,
                )
            status = 200
        case "POST", "team_member_remove":
            remove_member_form = RemoveTeamMemberForm(
                workspace, data=request.POST
            )
            if not remove_member_form.is_valid():
                return HttpResponse(_("Invalid form data"), status=400)
            team_member = remove_member_form.cleaned_data["team_member"]
            try:
                team_member_delete(team_member=team_member, who=request.user)
            except serializers.ValidationError as error:
                return HttpResponse(
                    _("Failed to remove team member: {error}").format(
                        error=str(error)
                    ),
                    status=400,
                )
            status = 200
        case _:
            status = 200

    if request.method == "POST":
        workspace = workspace_find_by_workspace_uuid(
            who=request.user, workspace_uuid=workspace_uuid, qs=workspace_qs
        )
        assert workspace

    context = {
        **_get_workspace_settings_context(
            request=request, workspace=workspace, active_tab="team"
        ),
        "invite_form": InviteTeamMemberForm(),
        "remove_form": RemoveTeamMemberForm(workspace=workspace),
        "uninvite_form": UninviteTeamMemberForm(),
        **additional_context,
    }

    return render(request, template, context=context, status=status)


class TeamMemberUpdateForm(forms.ModelForm):
    """Form for updating team member roles and job title."""

    class Meta:
        """Meta."""

        model = TeamMember
        fields = "role", "job_title"
        widgets = {
            "role": forms.RadioSelect(),
            "job_title": forms.TextInput(
                attrs={"placeholder": _("Enter job title")}
            ),
        }


@require_http_methods(["GET", "POST"])
@platform_view
def workspace_settings_team_member_update(
    request: AuthenticatedHttpRequest,
    workspace_uuid: UUID,
    team_member_uuid: UUID,
) -> HttpResponse:
    """Update a team member's role."""
    workspace = workspace_find_by_workspace_uuid(
        who=request.user,
        workspace_uuid=workspace_uuid,
        qs=WorkspaceDetailQuerySet,
    )
    if workspace is None:
        raise Http404(_("Workspace not found"))

    team_member = team_member_find_by_team_member_uuid(
        who=request.user, team_member_uuid=team_member_uuid
    )
    if team_member is None or team_member.workspace != workspace:
        raise Http404(_("Team member not found"))

    context = {
        **_get_workspace_settings_context(
            request=request, workspace=workspace, active_tab="team"
        ),
        "team_member": team_member,
    }

    match request.method:
        case "POST":
            form = TeamMemberUpdateForm(
                data=request.POST, instance=team_member
            )
            if not form.is_valid():
                context = {**context, "form": form}
                status = 400

            try:
                team_member_update(
                    who=request.user,
                    team_member=team_member,
                    job_title=form.cleaned_data.get("job_title"),
                )
                return redirect(
                    "dashboard:workspaces:team-members", workspace.uuid
                )
            except serializers.ValidationError as error:
                populate_form_with_drf_errors(form, error)
                context = {**context, "form": form}
                status = 400
        case _:
            form = TeamMemberUpdateForm(instance=team_member)
            context = {**context, "form": form}
            status = 200
    return render(
        request,
        "workspace/workspace_settings_team_member_update.html",
        context=context,
        status=status,
    )


class WorkspaceCouponForm(forms.Form):
    """Form for adding a coupon to a workspace."""

    code = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={"placeholder": _("Enter coupon code")}),
        label=_("Coupon code"),
    )


class WorkspaceBillingForm(forms.Form):
    """Checkout form."""

    seats = forms.IntegerField(
        min_value=1,
        max_value=100,
        widget=forms.NumberInput(
            attrs={"placeholder": _("Number of workspace seats")}
        ),
        label=_("Workspace seats"),
    )


# XXX this should be in the corporate app
@require_http_methods(["POST"])
@platform_view
def workspace_settings_billing_edit(
    request: AuthenticatedHttpRequest, workspace_uuid: UUID
) -> HttpResponse:
    """Redirect user to Stripe billing portal."""
    customer = customer_find_by_workspace_uuid(
        workspace_uuid=workspace_uuid, who=request.user
    )
    if customer is None:
        raise Http404(_("Workspace or customer not found"))

    try:
        session = create_billing_portal_session_for_customer(
            customer=customer, who=request.user
        )
    except serializers.ValidationError:
        # TODO show a more meaningful error
        return HttpResponseBadRequest()
    return redirect(session.url)


# XXX REFACTOR ME
PRICE_PER_SEAT = 8


# XXX the part that accepts POST should be in the corporate app instead
# TODO figure out how to break this apart
@require_http_methods(["GET", "POST"])
@platform_view
def workspace_settings_billing(
    request: AuthenticatedHttpRequest, workspace_uuid: UUID
) -> HttpResponse:
    """Show workspace billing settings."""
    workspace = workspace_find_by_workspace_uuid(
        who=request.user,
        workspace_uuid=workspace_uuid,
        qs=WorkspaceDetailQuerySet,
    )
    if workspace is None:
        raise Http404(_("Workspace not found"))
    workspace.quota = workspace_get_all_quotas(workspace)

    context = _get_workspace_settings_context(
        request=request, workspace=workspace, active_tab="billing"
    )

    template = "workspace/workspace_settings_billing.html"
    context = {
        **context,
        "billing_form": WorkspaceBillingForm(),
        "coupon_form": WorkspaceCouponForm(),
    }

    match (
        request.method,
        request.POST.get("action"),
        workspace.customer.subscription_status,
    ):
        case "GET", _, _:
            if workspace.customer.subscription_status == "ACTIVE":
                quota = workspace.quota.team_members_and_invites
                seats_remaining = (quota.limit or 0) - (quota.current or 0)
                context = {
                    **context,
                    "monthly_total": workspace.customer.seats * PRICE_PER_SEAT,
                    "seats_remaining": seats_remaining,
                    "price_per_seat": PRICE_PER_SEAT,
                }

            return render(request, template, context=context)
        case "POST", _, "ACTIVE":
            return HttpResponseBadRequest(
                _(
                    "You've already activated a subscription for this workspace"
                ),
            )
        case "POST", "checkout", _:
            billing_form = WorkspaceBillingForm(request.POST)
            if not billing_form.is_valid():
                context = {**context, "billing_form": billing_form}
                return render(request, template, context=context, status=400)
            try:
                session = customer_create_stripe_checkout_session(
                    customer=workspace.customer,
                    who=request.user,
                    seats=billing_form.cleaned_data["seats"],
                )
            except serializers.ValidationError as e:
                populate_form_with_drf_errors(billing_form, e)
                context = {**context, "billing_form": billing_form}
                return render(request, template, context=context, status=400)
            return redirect(session.url)
        case "POST", "redeem_coupon", _:
            coupon_form = WorkspaceCouponForm(request.POST)
            if not coupon_form.is_valid():
                context = {**context, "coupon_form": coupon_form}
                return render(request, template, context=context, status=400)
            try:
                coupon_redeem(
                    who=request.user,
                    code=coupon_form.cleaned_data["code"],
                    workspace=workspace,
                )
            except serializers.ValidationError as e:
                populate_form_with_drf_errors(coupon_form, e)
                context = {**context, "coupon_form": coupon_form}
                return render(request, template, context=context, status=400)
            return redirect("dashboard:workspaces:billing", workspace.uuid)
        case _:
            return HttpResponseBadRequest(_("Expected action"))


QuotaEntry = TypedDict("QuotaEntry", {"label": str, "quota": Quota})


@platform_view
def workspace_settings_quota(
    request: AuthenticatedHttpRequest, workspace_uuid: UUID
) -> HttpResponse:
    """Show workspace quota."""
    workspace = workspace_find_by_workspace_uuid(
        who=request.user,
        workspace_uuid=workspace_uuid,
        qs=WorkspaceDetailQuerySet,
    )
    if workspace is None:
        raise Http404(_("Workspace not found"))
    workspace.quota = workspace_get_all_quotas(workspace)

    context = _get_workspace_settings_context(
        request=request, workspace=workspace, active_tab="quota"
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

    context = {**context, "quota_rows": quota_rows}
    return render(
        request, "workspace/workspace_settings_quota.html", context=context
    )
