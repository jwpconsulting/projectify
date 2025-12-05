---
title: SvelteKit Frontend removal plan - modal views
---
<!--
SPDX-FileCopyrightText: 2025 JWP Consulting GK

SPDX-License-Identifier: AGPL-3.0-or-later
-->

This document outlines what overlays and dialogs we have to create in the
Django the new frontend to
achieve feature parity with the previous frontend.

# Modal views

These views are parts of the UI that don't have their own page and interact
with the page that they're placed on

The side navigation has these components:

- **Side nav labels**: Create and update labels, accessible from side nav when logged in
  and interacting with a workspace. You can also filter tasks by labels here
- **Side nav team members**: Filter tasks by users, including tasks that aren't assigned to
  anyone

Projectify has these overlays for creating, deleting, updating resources.
Overlays are accessible from the dashboard, task pages, and workspace settings.

- **Create new section**: Enter a section name to create a new section
- **Create project**: Enter a project name to create a new project
- **Archive project**: Puts a project into the workspace project archive
- **Delete task**: Deletes a task with its subtasks and all other attached data
- **Edit project**: Change a project's name
- **Edit section**: Change a section's name
- **Recover project**: Recover a project from the workspace project archive
- **Delete project**: Delete an archived project
- **Delete section**: Delete a section including its tasks

The **team members** workspace settings screen has a modal team member **role
assignment** dropdown.

The navigation header turns into an **overlay menu** on narrow (mobile)
screens.

The **Modal migration** section describes how to port each overlay.

# Context menus

Further, the SvelteKit frontend has these context menus:

- **User profile** context menu (**log out**, **My profile**)
- **Workspace** context menu (select the workspace)
- **Side navigation** context menu (workspace settings, archive, minimize
  sidebar)
- **Section** context menu (edit/delete/change order)
- **Task** context menu (described in [./remove-fe.md](./remove-fe.md)
- **Task label** context menu (dashboard and task view)
- **Task assignee** context menu (dashboard and task view)

The **Context menu migration** section describes how to port each context menu

# Modal migration

## Side navigation labels

### Create and update

Move label creation and updating to the workspace settings for now. Where
necessary, add a new link to "Create or update labels".

### Filter

Show somewhere what labels are assigned to what tasks? Make label filter
clickable and update query params instead?

## Side navigation team members

Either we make buttons that add GET query params to the url, or we incorporate
user filtering into the Task search field.

## Create section

For consistency, we rename this overlay to **Create section**.

- **View**: Create view with the address `/dashboard/project/<uuid:project_uuid>/create-section`
- **Link**: Turn existing **Add section** button on project page into link to
  the address, change the button to say **Create section**
- **Form contents**:
  - Show a form with title and description fields
  - **Add section**: Submit the form
  - **Cancel**: Return to project
- **Success**: Redirect to project and scroll to section
- **Failure**: Render form with errors

## Create project

Done on 2025-12-01.

- **View**: Create view with the address `/dashboard/workspace/<uuid:workspace_uuid>/create-project`
- **Link**: Copy **Create new project** button from old frontend and link to
  the address
- **Form contents**:
  - Show a form with title and description fields
  - **Create project**: Submit the form
  - **Cancel**: Go to first available project in workspace, if no project
    exists, go to project settings inside workspace settings
- **Success**: Redirect to new project on success
- **Failure**: Render form with errors

## Delete task

- **Link**: On the task page, create a **Delete Task** red button next to **Edit**
- Show HTMX confirm dialog when user pressed **Delete Task**. Delete task on
  confirmation.

## Archive project

Done on 2025-12-01.

Instead of archiving projects from the context menu, we want to create a new
settings screen that lets you archive projects.

- **View**: Create a project settings view with the address
  `/dashboard/workspace/<uuid:workspace_uuid>/settings/projects`
- **Link**: Place **Projects** tab in workspace settings tab list
- **Page contents**:
  - Show active projects in a list. Active projects are projects that the user hasn't archived.
  - Show a **Update** and **Archive** button for every active project.
  - When pressing the **Update** button, redirect to this address: `/dashboard/project/<uuid:project_uuid>/update`
    For more details, see the following **Rename project** section.
  - When pressing the **Archive** button, show a confirmation screen. When the
  user presses **Ok**, the project becomes inactive.
  - Show archived projects in the bottom with a **Recover** and **Delete**
    button for every archived project
  - When pressing the **Recover** button, show a confirmation screen. When the
  user presses **Ok**, the project goes back to the active projects
  - When pressing the **Delete** button, show a confirmation screen. When the
  user presses **Ok**, it deletes the project.

## Update project

Done on 2025-12-01.

- **View**: Create an update project view with the address `/dashboard/project/<uuid:project_uuid>/update`
- **Link**: Link to this page from the **Update** link on the project
  settings view
- **Form contents**:
  - Show project title and description fields
  - **Update project**: Save the form contents to the project. Redirect back to project
    settings.
  - **Cancel**: Go back to project settings

## Update section

This replaces the **Edit section title** modal.

- **View**: Create an update section view with the address `/dashboard/section/<uuid:section_uuid>/update`
- **Link**: Change the ellipsis button in the section header to link to this view
- **Form contents**:
  - Show section title and description fields
  - **Save**: Save the form contents to the section. Redirect back to
  the section's project and scroll to the section
  - **Cancel**: Discard the form contents. Redirect back to the project's
  section and scroll to the section.
- **Section move** form:
  - **Move up**: Move the section above the previous section
  - **Move down**: Move the section below the next section
- **Delete** button: Show a confirmation dialog. If the user presses **Ok**,
  delete the section.

## Project archive

Incorporate this into the project settings tab in the workspace settings.
See the **Archive project** and **Recover project** section in this
document.

# Context menus

## User profile

Change **log out**, **My profile** into individual links

## Workspace

Turn the workspace select context menu into a collapsible menu with
links that point to one workspace each.

## Side navigation

Replace the following items with equivalent features:

- **Minimise sidebar**: Remove this button and any side navigation minimise
  feature.
- **Go to archive**: Access the archive by going to the workspace settings
- **Workspace settings**: Access the workspace settings by pressing the ellipsis
icon. TODO: Consider using a different icon or using words

## Section context menu

- **Ordering**: The **update section** page has **move up** and **move
  down** buttons as a replacement
- **Collapse section**: We implement no replacement for this.
- **Edit section title**: The **update section** page has a form for updating
  the section's title.
- **Delete section**: The **update section** page has a **delete section**
  link. Show an HTMX confirmation dialog and delete the section when the user
  presses **Ok***.

## Task

Here's how to replace items in the task context menu with equivalent UI features:

- **Open task**: No replacement
- **Move task**: Change the ellipsis (`...`) button in the task card or line to
  link to a new **Task actions** page. See the **Task actions** section for a
  description.
- **Copy link**: No replacement
- **Delete task**: Add a delete button to the task page.

### Task actions

- **View**: Create a new view with the address
  `/dashboard/task/<uuid:task_uuid>/actions`
- **Link** to this view from a task card in the project view
- **Page contents**:
  - **Section move form**:
    - Dropdown with **section** names
    - **Move to section** button
    - When the user presses **Move to section**, move the task to that section
      and redirect the user to the task's project and scroll to the task.
  - **Move to top / bottom**:
    - **Move to top** button
    - **Move to bottom** button
    - When the user presses one of these buttons, move the task to the top
    or bottom of the task's current section accordingly. Redirect the user back
    to the task's project and scroll to the task.
  - **Delete task**: When the user presses this, show an HTMX confirm dialog
    and delete the task

## Label assignment

Remove and add back in a future Projectify revision. Users can still edit
labels from the task edit page.

## Team member assignment

Remove and add back in a future Projectify revision. Users can still edit
the assignee from the task edit page.

## Mobile navigation overlay

Remove entirely for now. Tweak layout to work with mobile.
