# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2025 JWP Consulting GK
"""Onboarding Views."""

from uuid import UUID

from django import forms
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from projectify.user.models import User


def welcome(request: HttpRequest) -> HttpResponse:
    """Serve onboarding welcome page."""
    return render(request, "onboarding/welcome.html")


class PreferredNameForm(forms.ModelForm):
    """Update User's preferred name."""

    class Meta:
        model = User
        fields = ["preferred_name"]


@require_http_methods(["GET", "POST"])
def about_you(request: HttpRequest) -> HttpResponse:
    """
    Add a preferred name and profile picture for the current user,

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
            # TODO: error messages?
            return HttpResponseRedirect("/onboarding/new-workspace")
    else:
        form = PreferredNameForm(instance=request.user)

    return render(request, "onboarding/about_you.html", {"form": form})


@require_http_methods(["GET", "POST"])
def new_workspace(request: HttpRequest) -> HttpResponse:
    """
    Create a new workspace.

    GET:
    Show page with workspace creation form
    POST:
    On success: Create a new workspace. Redirect user to
    /onboarding/new-project/<workspace-uuid> with the workspace UUID coming
    from the newly created workspace.
    """
    return render(request, "onboarding/new_workspace.html")


@require_http_methods(["GET", "POST"])
def new_project(request: HttpRequest, workspace_uuid: UUID) -> HttpResponse:
    """
    Create a new project inside the newly created workspace.

    GET: Show project creation form for `workspace_uuid`
    POST:
    On success: Create new project inside the workspace. Redirect user to
    /onboarding/new-task/<project-uuid> with the project UUID coming from the
    newly created project.
    On error: Show project creation form with errors.
    """
    return HttpResponse("TODO")


@require_http_methods(["GET", "POST"])
def new_task(request: HttpRequest, project_uuid: UUID) -> HttpResponse:
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
    return HttpResponse("TODO")


@require_http_methods(["GET", "POST"])
def new_label(request: HttpRequest, task_uuid: UUID) -> HttpResponse:
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
    return HttpResponse("TODO")


def assign_task(request: HttpRequest, task_uuid: UUID) -> HttpResponse:
    """Show the user that Projectify assigned the task to them."""
    return HttpResponse("TODO")
