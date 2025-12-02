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
# DONE
# GET: Render accessibility statement
accessibility(request)

# DONE
# GET: Show contact information
contact_us(request)

# TODO
# GET: Show credits
credits(request)

# DONE
# GET: Show free software license information
free_software(request)

# DONE
# GET: Show pricing information
pricing(request)

# TODO
# GET: Show the privacy policy
privacy(request)

# DONE
# GET: Show the vulnerability disclosure policy
security_disclose(request)

# DONE
# GET: Show general security information
security_general(request)

# DONE
# GET: Show use cases for Projectify
solutions_index(request)

# DONE
# GET: Show a specific use case
solutions_detail(request, page: str)

# TODO
# GET: Show terms of service
tos(request)
```

## Help

This is separate from the storefront pages to make organizing the markdown help
documents easier.

In `backend/projectify/help/views.py`, add the following views:

```python
# DONE
# GET: Render help overview
help_index(request)

# DONE
# GET: Show help page for topic `page`
help_detail(request, page: str)
```

# Onboarding

All views during onboarding require the user to be logged in.

In `backend/projectify/onboarding/views.py`, add the following views:

```python
# DONE
# Add a preferred name and profile picture for the current user
# GET:           Show page with form
# POST: SUCCESS: Update user profile. Redirect user to
#                /onboarding/new-workspace
#       FAILURE: Show this page again with errors
about_you(request)

# DONE
# Create a new workspace.
# GET:           Show page with workspace creation form
# POST: SUCCESS: Create a new workspace. Redirect user to
#                /onboarding/new-project/<workspace-uuid> with the workspace
#                UUID coming from the newly created workspace.
new_workspace(request)

# DONE
# Create a new project inside the newly created workspace.
# GET:           Show project creation form for `workspace_uuid`
# POST: SUCCESS: Create new project inside the workspace. Redirect user to
#                /onboarding/new-task/<project-uuid> with the project UUID
#                coming from the newly created project.
#       FAILURE: Show project creation form with errors
new_project(request, workspace_uuid)

# DONE
# Create a new task inside the newly created project.
# Put the task in a "To Do" section. Create this section before creating the
# task.
# GET:           Show task creation form for project `project_uuid`
# POST: SUCCESS: Creates a section and task and assigns it to the user.
#                Redirect user to onboarding/new-label/<task-uuid> with the
#                task uuid coming from the newly created task
#       FAILURE: Show task creation form with errors
new_task(request, project_uuid)

# DONE
# Ask the user to give the newly created task a label.
# GET:           Show label creation form for task `task_uuid`
# POST: SUCCESS: Creates a label and adds it to the task. Redirect to
#                onboarding/assign-task/<task_uuid>.
#       FAILURE: Show label creation form with errors
new_label(request, task_uuid)

# DONE
# GET: Show the user that Projectify assigned the task to them.
assign_task(request, task_uuid)
```

# Platform

All views in platform require the user to be logged in.

## Dashboard general views

In `backend/projectify/workspace/views/dashboard.py`, implement the following
view functions:

```python
# TODO, right now it shows available workspaces
# GET: Redirect user to first available workspace and project
dashboard(request)
```

## Project
In `backend/projectify/workspace/views/project.py`, implement the following
view functions:

```python
# DONE
# GET: Show a project and its tasks
project_detail_view(request, project_uuid)

# DONE
# GET:  Show a project creation form
# POST: Create a new project for the given `workspace_uuid`
project_create_view(request, workspace_uuid)

# DONE
# GET:  Show a project information update form
# POST: Update the project
project_update_view(request, project_uuid)

# DONE
# POST: Set the project with UUID `project_uuid` to archived
project_archive_view(request, project_uuid)

# DONE
# POST: Set the project with UUID `project_uuid` to active
project_recover_view(request, project_uuid)

# DONE
# POST: Delete the archived project with UUID `project_uuid`
project_delete_view(request, project_uuid)
```

## Section

In `backend/projectify/workspace/views/section.py`, implement the following
view functions:

```python
# TODO
# GET: Redirect to project with this section visible
section(request, section_uuid)

# DONE
# GET:  Shows section update form
# POST: Depending on the action:
# "save":      update the section
# "move_up":   move it above the previous section
# "move_down": move it below the next section
section_update_view(request, section_uuid)
```

## Task

In `backend/projectify/workspace/views/task.py`, implement the following view
functions:

```python
# DONE
# GET: Render a form for creating `sub_tasks` sub tasks
task_create_sub_task_form(request, sub_tasks)

# DONE
# GET:  Shows task creation form
# POST: Creates task within section
task_create(request, section_uuid)

# DONE
# GET: Show task with UUID `task_uuid`
task_detail(request, task_uuid)

# DONE
# GET:  Show task update form
# POST: Updates task
task_update_view(request, task_uuid)

# DONE
# POST: Move a task up or down
task_move(request, task_uuid)
```

## Workspace

In `backend/projectify/workspace/views/workspace.py`, implement the following
view functions:

```python
# TODO
# GET: Redirects user to first available project within workspace
workspace(request)

# DONE
# GET:  Shows workspace
# POST: Updates workspace
workspace_settings(request, workspace_uuid)

# DONE
# GET:  Shows projects in workspace for editing
# Note: The old frontend doesn't implement this page and instead
#       had a workspace project archive page. To simplify implementing
#       the new version, editing projects and archiving/deleting projects
#       become part of the following view.
worskpace_settings_projects(request, workspace_uuid)

# DONE
# GET: List team members
workspace_settings_team_members(request, workspace_uuid)

# POST: Invite a team member
workspace_settings_team_members_invite(request, workspace_uuid)

# DELETE: Remove a team member
workspace_settings_team_members_remove(request, workspace_uuid, team_member_uuid)

# POST: Uninvite a team member
workspace_settings_team_member_uninvite(request, workspace_uuid)

# POST: Create and redirect to billing portal session
workspace_settings_billing_edit(request, workspace_uuid)

# GET:  Review current billing information
# POST: Start stripe checkout or redeem coupon
workspace_settings_billing(request, workspace_uuid)

# GET: Review workspace resource quota
workspace_settings_quota(request, workspace_uuid)
```

Current, intermediate implementation is:

```python
# TODO REMOVE
# GET: Show a list of workspaces that the current user can access
workspace_list_view(request)

# TODO REMOVE
# GET: Show the workspace's projects
workspace_view(request, workspace_uuid)
```

## User

In `backend/projectify/user/views/user.py`, implement the following views:

```python
# DONE
# GET:  Show user profile information
# POST: Change name, profile picture
user_profile(request)

# DONE
# GET:  Show password change form
# POST: Change password
password_change(request)

# DONE
# GET:  Show email change form
# POST: Initiate email update
email_address_update(request)

# DONE
# GET:  Confirm email update with `token`
email_address_update_confirm(request, token)

# DONE
# GET: Show confirmation that user initiated email change
email_address_update_requested(request)

# DONE
# GET: Show confirmation that user has changed email
email_address_update_confirmed(request)
```
