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

### Filter by labels

Add filter by label function to **Task search** panel. Use checkboxes inside
a collapsible HTML element. Show number of tasks next to label names.

### List workspace labels

Create a new page to manage all workspace labels:

- [ ] **Route**: `dashboard/workspace/[uuid]/settings/labels`
- [ ] **Page title**: `{workspace.title} labels - Projectify`
- [ ] **Contents**:
    - [ ] Table listing all labels
    - [ ] For each label, show:
        - [ ] Label **name**
        - [ ] Label **color**
        - [ ] Update form link
        - [ ] Delete button
    - [ ] Show an **Add label** button in the bottom

### Create label

Make a new page for creating a new label for a workspace

- [ ] **Route**: `dashboard/workspace/[uuid]/settings/labels/create`
- [ ] **Page title**: `Create label for {workspace.title} - Projectify`
- [ ] **Contents**:
    - [ ] **Name** input
    - [ ] **Color** selector (radio input)
    - [ ] **Create** button; redirects to **List workspace labels** on success
    - [ ] **Back** button; goes back to **List workspace labels** view

### Update label

- [ ] **Route**: `dashboard/labels/[uuid]`
- [ ] **Page title**: `Update {label.name} - Projectify`
- [ ] **Contents**:
    - [ ] **Name** input
    - [ ] **Color** selector (radio input)
    - [ ] **Update** button; redirects to **List workspace labels** on success
    - [ ] **Back** button; goes back to **List workspace labels** view

## Side navigation team members

Either we make buttons that add GET query params to the url, or we incorporate
user filtering into the Task search field.

## Create section (DONE)

For consistency, we rename this overlay to **Create section**.

- [x] **View**: Create view with the address `/dashboard/project/<uuid:project_uuid>/create-section`
- [x] **Link**: Turn existing **Add section** button on project page into link to
  the address, change the button to say **Create section**
- [x] **Form contents**:
  - [x] Show a form with title and description fields
  - [x] **Create section**: Submit the form
  - [x] **Back**: *Go back to project* link
- [x] **Success**: Redirect to project and scroll to section
- [x] **Failure**: Render form with errors

## Create project (DONE)

- [x] **View**: Create view with the address `/dashboard/workspace/<uuid:workspace_uuid>/create-project`
- [x] **Link**: Copy **Create new project** button from old frontend side nav
  project list bottom. Make button anchor and link to the address
- [x] **Form contents**:
  - [x] Show a form with title and description fields
  - [x] **Create project**: Submit the form
  - [x] **Link**: Show *Go to workspace settings* link.
- [x] **Success**: Redirect to new project on success
- [x] **Failure**: Render form with errors

Things that are left to do:

- [x] Populate side nav with `workspace` and `projects` context objects

## Delete task

- [ ] **Link**: On the task page, create a **Delete Task** red button next to **Edit**
- [ ] Show HTMX confirm dialog when user pressed **Delete Task**. Delete task on
  confirmation.

## Archive project (DONE)

Instead of archiving projects from the context menu, we want to create a new
settings screen that lets you archive projects.

- [x] **View**: Create a project settings view with the address
  `/dashboard/workspace/<uuid:workspace_uuid>/settings/projects`
- [x] **Link**: Place **Projects** tab in workspace settings tab list
- [x] **Page contents**:
  - [x] Show active projects in a list. Active projects are projects that the user hasn't archived.
  - [x] Show a **Update** and **Archive** button for every active project.
  - [x] When pressing the **Update** button, redirect to this address: `/dashboard/project/<uuid:project_uuid>/update`
    For more details, see the following **Rename project** section.
  - [x] When pressing the **Archive** button, show a confirmation screen. When the
  user presses **Ok**, the project becomes inactive.
  - [x] Show archived projects in the bottom with a **Recover** and **Delete**
    button for every archived project
  - [x] When pressing the **Recover** button, show a confirmation screen. When the
  user presses **Ok**, the project goes back to the active projects
  - [x] When pressing the **Delete** button, show a confirmation screen. When the
  user presses **Ok**, it deletes the project.

Things that are left to do:

- [x] Style section headers **Projects** and **Archived projects**
- [x] Style **Archive**, **Recover**, **Delete** buttons

## Update project (DONE)

- [x] **View**: Create an update project view with the address `/dashboard/project/<uuid:project_uuid>/update`
- [x] **Link**: Link to this page from the **Update** link on the project
  settings view
- [x] **Form contents**:
  - [x] Show project **title** and **description** fields
  - [x] **Update project**: Save the form contents to the project. Redirect back to project
    settings.
  - [x] **Go back**: Go back to project settings

Things that are left to do:

- [x] Populate `projects` context variable

## Update section

Missing: Delete button, style link; Justus 2025-12-05

This replaces the **Edit section title** modal.

- [x] **View**: Create an update section view with the address `/dashboard/section/<uuid:section_uuid>/update`
- [x] **Link**: Change the ellipsis `...` button to a pencil button next to the
  section title with `aria-label`.
- [x] **Form contents**:
  - [x] Show section **title** and **description** fields
  - [x] **Update section**: Save the form contents to the section. Redirect back to
  the section's project and scroll to the section
  - [x] **Go back**: Discard the form contents. Redirect back to the project's
  section and scroll to the section.
- [x] **Section move** form:
  - [x] **Move up**: Move the section above the previous section
  - [x] **Move down**: Move the section below the next section
- [x] **Delete** button: Show a confirmation dialog. If the user presses **Ok**,
  delete the section.

## Project archive

DONE

Incorporate this into the project settings tab in the workspace settings.
See the **Archive project** and **Recover project** section in this
document.

# Context menus

## User profile

Change the following into individual links:

- [x] **Log out**
- [x] **My profile**

## Workspace

- [ ] Create collapsible menu
- [ ] Turn the workspace select context menu into a collapsible menu with
links that point to one workspace each.

## Side navigation

Replace the following items with equivalent features:

- [x] **Minimise sidebar**: Remove this button and any side navigation minimise
  feature.
- [x] **Go to archive**: Access the archive by going to the workspace settings
  and then pressing the **Projects** tab
- [x] **Workspace settings**: Access the workspace settings by pressing the ellipsis
icon.
- [ ] Consider using a different icon or using words for the **Workspace
  settings** button

## Section context menu

- [x] **Ordering**: The **update section** page has **move up** and **move
  down** buttons as a replacement
- [x] **Collapse section**: We implement no replacement for this.
- [x] **Edit section title**: The **update section** page has a form for updating
  the section's title.
- **Delete section**: See **Update section**

## Task

Here's how to replace items in the task context menu with equivalent UI features:

- [x] **Open task**: No replacement
- [ ] **Move task**: Change the ellipsis (`...`) button in the task card or line to
  link to a new **Task actions** page. See the **Task actions** section for a
  description.
- [x] **Copy link**: No replacement
- [ ] **Delete task**: Add a delete button to the task page.

### Task actions

- [ ] **View**: Create a new view with the address
  `/dashboard/task/<uuid:task_uuid>/actions`
- [ ] **Link** to this view from a task card in the project view
- [ ] **Page contents**:
  - [ ] **Section move form**:
    - [ ] Dropdown with **section** names
    - [ ] **Move to section** button
    - [ ] When the user presses **Move to section**, move the task to that section
      and redirect the user to the task's project and scroll to the task.
  - [ ] **Move to top / bottom**:
    - [ ] **Move to top** button
    - [ ] **Move to bottom** button
    - [ ] When the user presses one of these buttons, move the task to the top
    or bottom of the task's current section accordingly. Redirect the user back
    to the task's project and scroll to the task.
  - [ ] **Delete task**: When the user presses this, show an HTMX confirm dialog
    and delete the task

## Label assignment

Remove and add back in a future Projectify revision. Users can still edit
labels from the task edit page.

## Team member assignment

Remove and add back in a future Projectify revision. Users can still edit
the assignee from the task edit page.

## Mobile navigation overlay

Remove entirely for now. Tweak layout to work with mobile.
