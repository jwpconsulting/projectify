---
title: Replacement Django view functions
---

<!--
SPDX-FileCopyrightText: 2025 JWP Consulting GK

SPDX-License-Identifier: AGPL-3.0-or-later
-->

This document details the Django views that are necessary to replace the Svelte
frontend.

Refer to `docs/remove-fe-pages.md` for a list of all pages that you have to
recreate.

Where overlays where used to create resources, create new views instead. For
example, users create sections using a section `ConstructiveOverlay`
in the SvelteKit frontend. Instead, a new `section_create` view offers this
feature on a separate page. This simplifies page navigation, usability, and
accessibility.

Where context menus are used to manipulate resources, create new views instead.
For example, users can move tasks up or down, or to different sections
using the task context menu. Create a new `task_context_menu` view to
achieve this in a new page instead. This view presents a form with
buttons to perform actions on a given task. When the user submits the form,
the backend performs the desired action, such as moving a task up or down.

# Storefront

In `backend/projectify/storefront/views.py`, add the following views:

```python
def accessibility(request: HttpRequest) -> HttpResponse: pass
def contact_us(request: HttpRequest) -> HttpResponse: pass
def credits(request: HttpRequest) -> HttpResponse: pass
def ethicalads(request: HttpRequest) -> HttpResponse: pass
def free_software(request: HttpRequest) -> HttpResponse: pass
def pricing(request: HttpRequest) -> HttpResponse: pass
def privacy(request: HttpRequest) -> HttpResponse: pass
def security_disclose(request: HttpRequest) -> HttpResponse: pass
def security_general(request: HttpRequest) -> HttpResponse: pass
def solutions_index(request: HttpRequest) -> HttpResponse: pass
def solutions_detail(request: HttpRequest, page: str) -> HttpResponse: pass
def tos(request: HttpRequest) -> HttpResponse: pass
```

## Help

This is separate from the storefront pages to make organizing the markdown help
documents easier.

In `backend/projectify/help/views.py`, add the following views:

```python
def help_index(request: HttpRequest) -> HttpResponse: pass
def help_detail(request: HttpRequest, page: str) -> HttpResponse: pass
```

# Onboarding

All views during onboarding require the user to be logged in.

In `backend/projectify/onboarding/views.py`, add the following views:

```python
@require_http_methods(["GET", "POST"])
def about_you(request: HttpRequest) -> HttpResponse:
    """
    Add a preferred name and profile picture for the current user,

    GET:
    Show page with form
    POST:
    On success: Update user profile. Redirect user to /onboarding/new-workspace
    On failure: Show this page again with errors
    """

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


@require_http_methods(["GET", "POST"])
def new_project(request: HttpRequest, workspace_uuid: UUID) -> HttpResponse:
    """
    Create a new project inside the newly created workspace.

    GET: Show project creation form for `workspace_uuid`
    POST:
    On success: Create new project inside the workspace. Redirect user to
    /onboarding/new-task/<project-uuid> with the project UUID coming from the
    newly created project.
    On error: Show project creation form with errors
    """


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
    On error: Show task creation form with errors
    """

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
    Show label creation form with errors
    """

def assign_task(request: HttpRequest, task_uuid: UUID) -> HttpResponse:
    """Show the user that Projectify assigned the task to them."""
```

# Platform

All views in platform require the user to be logged in.

## Dashboard general views

In `backend/projectify/workspace/views/dashboard.py`, implement the following
view functions:

```python
# Redirect user to first available workspace and project
def dashboard(request: HttpRequest) -> HttpResponse: pass
```

## Project

## Section

In `backend/projectify/workspace/views/section.py`, implement the following
view functions:

```python
# Redirect to project with this section visible
def section(request: HttpRequest, section_uuid: UUID) -> HttpResponse: pass
@require_http_methods(["GET", "POST"])
# GET: Shows section update form
# POST: Updates section
def section_update(request: HttpRequest, section_uuid: UUID) -> HttpResponse: pass
@require_http_methods(["POST"])
# POST: Moves section up or down
def section_move(request: HttpRequest, section_uuid: UUID) -> HttpResponse: pass
```

## Task

In `backend/projectify/workspace/views/task.py`, implement the following view
functions:

```python

# GET: Render a form for creating `sub_tasks` sub tasks
task_create_sub_task_form(request, sub_tasks)

# GET: Shows task creation form
# POST: Creates task within section
task_create(request, section_uuid)

# Show a task
task_detail(request, task_uuid)

# GET: Shows task update form
# POST: Updates task
task_update_view(request, task_uuid)

# POST: Move a task up or down
task_move(request, task_uuid)
```

## Workspace

In `backend/projectify/workspace/views/workspace.py`, implement the following
view functions:

```python
# Redirects user to first available project within workspace
def workspace(request: HttpRequest) -> HttpResponse: pass

@require_http_methods(["GET", "POST"])
# GET: Shows archive projects
# POST: Accepts a list of project UUIDs to restore
def workspace_archive(request: HttpRequest, workspace_uuid: UUID) -> HttpResponse: pass
@require_http_methods(["GET", "POST"])
# GET: Shows workspace
# POST: Updates workspace
def workspace_settings(request: HttpRequest, workspace_uuid: UUID) -> HttpResponse: pass
def workspace_billing(request: HttpRequest, workspace_uuid: UUID) -> HttpResponse: pass
def workspace_quota(request: HttpRequest, workspace_uuid: UUID) -> HttpResponse: pass
# GET: Shows team members
# POST: Changes or deletes team members
# POST: Invites team member (checks for which form is submitted)
def workspace_team_member(request: HttpRequest, workspace_uuid: UUID) -> HttpResponse: pass
```

## User
