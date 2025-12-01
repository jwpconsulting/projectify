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

These views are parts of the UI that don't have their own page.

- **Side nav labels**: Create and update labels, accessible from side nav when logged in
  and interacting with a workspace. You can also filter tasks by labels here
- **Side nav team members**: Filter tasks by users, including tasks that aren't assigned to
  anyone
- **Overlays**: Various creation/deletion/archival confirmation screens
  accessible from dashboard or task.
  - Add new section
  - Add new project
  - Archive project
  - Delete task
  - Rename project
  - Rename section
  - Restore project
- **Context menus**:
  - User profile context menu (logout/edit profile)
  - Workspace context menu (select the workspace)
  - Side navigation context menu (workspace settings, archive, minimize
    sidebar)
  - Section context menu (edit/delete/change order)
  - Task context menu (described in detail above)
  - Task label assignment (dashboard and task view)
  - Task user assignment (dashboard and task view)
- **Role assignment** in workspace settings
- **Overlay menus** that are only visible on narrow (mobile) screens.

# Migration plan

## Labels

### Create and update
Move label creation and updating to the workspace settings for now. Where
necessary, add a new link to "Create or update labels".

### Filter

Show somewhere what labels are assigned to what tasks? Make label filter
clickable and update query params instead?

## Users

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

## Add project

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

- **View**: Create view with the address `/dashboard/task/<uuid:task_uuid>/confirm-delete`
- **Link**: On the task page, create a **Delete Task** red button next to **Edit**
- **Contents**:
  - **Delete task** and **Cancel** button
  - When the user presses **Delete task** and deleting the task succeeds,
    redirect to the task's section. Show a confirmation flash message.
  - When the user presses **Cancel**, redirect back to the task.

## Archive project

Instead of archiving projects from the context menu, we want to create a new
settings screen that lets you archive projects.

- **View**: Create a project settings view with the address
  `/dashboard/workspace/<uuid:workspace_uuid>/settings/projects`
- **Link**: Place **Projects** tab in workspace settings tab list
- **Page contents**:
  - Show active projects in a list. Active projects are projects that the user hasn't archived.
  - Show a **Rename** and **Archive** button for every active project.
  - When pressing the **Rename** button, redirect to this address: `/dashboard/project/<uuid:project_uuid>/update`
    For more details, see the following **Rename project** section.
  - When pressing the **Archive** button, redirect to this address: `/dashboard/project/<uuid:project_uuid>/confirm-archive`
  - Show archived projects in the bottom with a **Recover** and **Delete**
    button for every archived project
  - When pressing the **Recover** button, redirect to this address:
    `/dashboard/project/<uuid:project_uuid/confirm-recover`
  - When pressing the **Delete** button, redirect to this address:
    `/dashboard/project/<uuid:project_uuid/confirm-delete`
- **Archive** page contents at `.../confirm-archive`:
  - **Archive** button: When the user presses this button and archiving the
    project succeeds, redirect to the first available project in the workspace.
    If all projects are archived, redirect to the projects settings view at
    `.../settings/projects`
  - **Cancel** button: Redirect the user back to the project settings view
- For the **Delete** page contents at `.../confirm-delete`, see the **Delete
  project** section.

## Rename project

- **View**: Create a rename view with the address `/dashboard/project/<uuid:project_uuid>/update`
- **Link**: Link to this page from the **rename** button on the project
  settings view
- **Form contents**:
  - Show project title and description fields
  - **Save**: Save the form contents to the project. Redirect back to project
    settings.
  - **Cancel**: Discard the form contents. Redirect back to project settings.

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
- **Delete** link: Redirect to the **delete section** view

## Recover project

- **View**: Create a new new view with the address
  `/dashboard/project/<uuid:project_uuid/confirm-recover`
- **Link**: Link to this address from the archived project list in the project
  settings
- **Form contents**:
  - **Recover** and **Cancel** buttons
- When pressing **Recover**, recover the project and redirect to the **project settings**
for the project's workspace
- When pressing **Cancel**, redirect to the project settings for the project's
  workspace

## Delete section

- **View**: Create a new view with the address
  `/dashboard/section/<uuid:section_uuid>/confirm-delete`
- **Link**: The **update section** page links to this view.
- **Form contents**:
  - **Delete** and **Cancel** buttons
- When pressing **Delete**, delete the section and redirect to the section's
  project page
- When pressing **Cancel**, redirect to the section's project and scroll to the
  section.

## Delete project

- **View**: Create a new view with the address
  `/dashboard/project/<uuid:project_uuid/confirm-delete`
- **Link**: The **Delete** button in the archived project list under the
  project settings links to this view
- **Form contents**:
  - **Delete** and **Cancel** buttons
- When pressing **Delete**, delete the project and redirect to the project
settings.
- When pressing **Cancel**, redirect to the project settings.

## Project archive

Incorporate this into the project settings tab in the workspace settings.
See the **Archive project** and **Recover project** section in this
document.

## Task context menu

Here's how to replace items in the task context menu with equivalent UI features:

- **Open task**: Remove this button
- **Copy link**: Remove this button
- **Move task**: Change the ellipsis (`...`) button in the task card or line to link to a new **Task actions** page. See the **Task actions** section
for a description.

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
  - **Delete task**: When the user presses this, redirect to the task
    `confirm-delete` screen

## Section context menu

- **Ordering**: The **update section** page has **move up** and **move
  down** buttons as a replacement
- **Collapse section**: We implement no replacement for this.
- **Edit section title**: The **update section** page has a form for updating
  the section's title.
- **Delete section**: The **update section** page has a **delete section** link

## Other

- **Minimize side nav**: Remove entirely
- Project page context menus:
  - **Label assignment**: Remove and add back in a future Projectify revision.
  - **Team member assignment**: Remove and add back in a future Projectify
    revision.
- **Mobile navigation overlay**: Remove entirely for now. Tweak layout to work with mobile.
