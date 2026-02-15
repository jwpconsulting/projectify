# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2025 JWP Consulting GK
"""Onboarding Views."""

from typing import Any
from uuid import UUID

from django import forms
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_http_methods

from projectify.lib.types import AuthenticatedHttpRequest
from projectify.user.models import User
from projectify.workspace.models.label import Label
from projectify.workspace.models.project import Project
from projectify.workspace.models.task import Task
from projectify.workspace.models.workspace import Workspace
from projectify.workspace.selectors.project import (
    ProjectDetailQuerySet,
    project_find_by_project_uuid,
)
from projectify.workspace.selectors.task import task_find_by_task_uuid
from projectify.workspace.selectors.team_member import (
    team_member_find_for_workspace,
)
from projectify.workspace.selectors.workspace import (
    WorkspaceDetailQuerySet,
    workspace_find_by_workspace_uuid,
    workspace_find_for_user,
)
from projectify.workspace.services.label import label_create
from projectify.workspace.services.project import project_create
from projectify.workspace.services.section import section_create
from projectify.workspace.services.task import (
    task_create_nested,
    task_update_nested,
)
from projectify.workspace.services.workspace import workspace_create


@login_required
def welcome(request: AuthenticatedHttpRequest) -> HttpResponse:
    """Serve onboarding welcome page."""
    return render(request, "onboarding/welcome.html")


class PreferredNameForm(forms.ModelForm):
    """Update User's preferred name."""

    class Meta:
        """Meta."""

        model = User
        fields = ["preferred_name"]


@login_required
@require_http_methods(["GET", "POST"])
def about_you(request: AuthenticatedHttpRequest) -> HttpResponse:
    """
    Add a preferred name and profile picture for the current user.

    GET:
    Show page with form
    POST:
    On success: Update user profile. Redirect user to /onboarding/new-workspace
    On failure: Show this page again with errors.
    """
    if request.method == "POST":
        form = PreferredNameForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            return redirect(reverse("onboarding:new_workspace"))
    else:
        form = PreferredNameForm(instance=request.user)

    context = {"form": form}
    return render(request, "onboarding/about_you.html", context)


class WorkspaceForm(forms.ModelForm):
    """Create a workspace."""

    title = forms.CharField(label=_("Workspace title"))

    class Meta:
        """Meta."""

        model = Workspace
        fields = ["title"]


@login_required
@require_http_methods(["GET", "POST"])
def new_workspace(request: AuthenticatedHttpRequest) -> HttpResponse:
    """
    Create a new workspace.

    GET:
    Show page with workspace creation form
    POST:
    On success: Create a new workspace. Redirect user to
    /onboarding/new-project/<workspace-uuid> with the workspace UUID coming
    from the newly created workspace.
    """
    if request.method == "POST":
        form = WorkspaceForm(request.POST)
        if form.is_valid():
            workspace = workspace_create(
                title=form.cleaned_data["title"],
                description=None,
                owner=request.user,
            )
            return redirect(
                reverse("onboarding:new_project", args=[str(workspace.uuid)])
            )
    else:
        form = WorkspaceForm()

    workspaces = workspace_find_for_user(who=request.user)

    context = {"form": form, "workspace": workspaces.first()}
    return render(request, "onboarding/new_workspace.html", context)


class ProjectForm(forms.ModelForm):
    """Create a project."""

    title = forms.CharField(label=_("Project title"))

    class Meta:
        """Meta."""

        model = Project
        fields = ["title"]


@login_required
@require_http_methods(["GET", "POST"])
def new_project(
    request: AuthenticatedHttpRequest, workspace_uuid: UUID
) -> HttpResponse:
    """
    Create a new project inside the newly created workspace.

    GET: Show project creation form for `workspace_uuid`
    POST:
    On success: Create new project inside the workspace. Redirect user to
    /onboarding/new-task/<project-uuid> with the project UUID coming from the
    newly created project.
    On error: Show project creation form with errors.
    """
    workspace = workspace_find_by_workspace_uuid(
        workspace_uuid=workspace_uuid, who=request.user, qs=WorkspaceDetailQuerySet
    )
    if workspace is None:
        raise Http404(_("Workspace not found"))

    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = project_create(
                who=request.user,
                workspace=workspace,
                title=form.cleaned_data["title"],
            )
            return redirect(
                reverse("onboarding:new_task", args=[str(project.uuid)])
            )
    else:
        form = ProjectForm()

    context = {
        "form": form,
        "workspace": workspace,
        "project": workspace.project_set.first(),
    }
    return render(request, "onboarding/new_project.html", context)


class TaskForm(forms.ModelForm):
    """Create a task."""

    title = forms.CharField(label=_("Task name"))

    class Meta:
        """Meta."""

        model = Task
        fields = ["title"]


@login_required
@require_http_methods(["GET", "POST"])
def new_task(
    request: AuthenticatedHttpRequest, project_uuid: UUID
) -> HttpResponse:
    """
    Create a new task inside the newly created project.

    Put the task in a To Do section. Create this section before creating the
    task.

    GET:
    Show task creation form for project `project_uuid`
    POST:
    On success: Creates a section and task and assigns it to the user. Redirect
    user to onboarding/new-label/<task-uuid> with the task uuid coming
    from the newly created task
    On error: Show task creation form with errors.
    """
    project = project_find_by_project_uuid(
        project_uuid=project_uuid,
        who=request.user,
        qs=ProjectDetailQuerySet,
    )
    if project is None:
        raise Http404(_("Project not found"))

    section = project.section_set.first()
    section_title = _("To do")
    if section:
        section_title = section.title
    context: dict[str, Any] = {
        "workspace": project.workspace,
        "project": project,
        "section": section,
        "section_title": section_title,
    }

    match request.method:
        case "GET":
            return render(
                request,
                "onboarding/new_task.html",
                {**context, "form": TaskForm()},
            )
        case "POST":
            pass
        case method:
            raise ValueError(f"Should not have hit method {method}")

    if section is None:
        section = section_create(
            who=request.user,
            title=section_title,
            description=None,
            project=project,
        )
    team_member = team_member_find_for_workspace(
        user=request.user, workspace=project.workspace
    )
    if not team_member:
        raise RuntimeError(
            f"No team_member found for current user in workspace {project.workspace.uuid}"
        )

    form = TaskForm(request.POST)
    if form.is_valid():
        task = task_create_nested(
            who=request.user,
            section=section,
            title=form.cleaned_data["title"],
            assignee=team_member,
            labels=[],
            sub_tasks={"create_sub_tasks": [], "update_sub_tasks": []},
        )
        return redirect(reverse("onboarding:new_label", args=[str(task.uuid)]))
    context = {**context, "form": form}
    return render(request, "onboarding/new_task.html", context)


class LabelForm(forms.ModelForm):
    """Create a label."""

    name = forms.CharField(label=_("Label name"))

    class Meta:
        """Meta."""

        model = Label
        fields = ["name"]


@login_required
@require_http_methods(["GET", "POST"])
def new_label(
    request: AuthenticatedHttpRequest, task_uuid: UUID
) -> HttpResponse:
    """
    Ask the user to give the newly created task a label.

    GET:
    Show label creation form for task `task_uuid`

    POST:
    On success:
    Creates a label and adds it to the task. Redirect to
    onboarding/assign-task/<task_uuid>.
    On failure:
    Show label creation form with errors.
    """
    task = task_find_by_task_uuid(task_uuid=task_uuid, who=request.user)
    if task is None:
        raise Http404(_("Task not found"))

    if request.method == "POST":
        form = LabelForm(request.POST)
        if form.is_valid():
            label = label_create(
                workspace=task.section.project.workspace,
                name=form.cleaned_data["name"],
                color=0,
                who=request.user,
            )
            task_update_nested(
                who=request.user,
                task=task,
                title=task.title,
                labels=[label],
                assignee=task.assignee,
            )

            return redirect(
                reverse("onboarding:assign_task", args=[str(task.uuid)])
            )
    else:
        form = LabelForm()
    context = {"form": form, "task": task}
    return render(request, "onboarding/new_label.html", context)


@login_required
def assign_task(
    request: AuthenticatedHttpRequest, task_uuid: UUID
) -> HttpResponse:
    """Show the user that Projectify assigned the task to them."""
    task = task_find_by_task_uuid(task_uuid=task_uuid, who=request.user)
    if task is None:
        raise Http404(_("Task not found"))
    context = {
        "task": task,
        "project": task.section.project,
        "workspace": task.section.project.workspace,
    }
    return render(request, "onboarding/assign_task.html", context)
