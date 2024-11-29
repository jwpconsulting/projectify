---
title: SvelteKit Frontend removal plan
---

SvelteKit SSR didn't turn out to be thing I thought it would be. Managing
global state through `getContext` and `setContext` means having to rewrite,
refactor and retest large parts of the application.

Continuing using Svelte and SvelteKit at this point is starting to look like I
am trapped inside a sunk cost fallacy.

# Goal

We already use Django for the backend. Let's fully embrace Django and also make
use of HTMX, which seems to be beloved

- Fully render frontend in Django using server side templates/views
- Remove dependency on SvelteKit and Svelte.
- Remove Django channels / WebSocket dependency

# How

- Use forms, views, templates in Django
- Use HTMX for interactive bit
- Remove frontend and reverse proxy completely

# Nice to have

- Figure out how to pack backend in single executable binary with `nix bundle`

# SWOT Analysis

## Strengths

- Rendering will be a lot faster
- Remove a vast amount of dependencies
- Simplify frontend rendering complexity
- Lack of interactive features - a feature, actually
- Greatly reduce size of things sent to browser
- JavaScript can be mostly eliminated - great
- Django is great and venerable
- Smaller footprint means fewer bugs.
- No more frontend/backend API type issues
- Core business logic was never part of frontend anyway. Any code that is
  duplicated can now be safely removed.

## Weaknesses

- This will take time. It's a 50% rewrite.
- Not guaranteed to improve product.
- It's complex. Vast re-retesting will be required.

## Opportunities

- Using Django and keeping everything monolithic makes moving forward so much
  more pleasant, I like Django, therefore fun.
- I can learn HTMX yay, fun.
- I might discover latent bugs that I can now fix, fixing bugs is fun.

## Risks

- Lack of HTMX experience, scary scary.
- New bugs or regressions, oh no.
- Lose motivation, this is totally real.
- Maybe it turns out SvelteKit was great for reasons I wasn't aware of yet,
  unlikely, but who knows. It might have been the glue that held everything
  together

# Rewrite steps

## Analysis

1. Test out HTMX. Thoroughly. Make sure you are comfortable.
2. Take inventory of all frontend pages
3. Identify remaining risks
4. Determine acceptance criteria.
5. Consider alternatives.
6. Understand if Tailwind can be used with Django
7. Find out way to use something like frontend components in Django.

## Planning

Subject to change.

1. Plan base template structure
2. Write out which views need to be created.
3. Write out which forms need to be created. See how DRF serializers can be
   turned into forms.
4. Write out which templates need to be created.
5. Identify all JavaScript only/frontend only functions that need to be
   recreated in Django

## Implementation

Subject to change.

1. Create views, templates and forms in tandem. Write test cases as you go.

- It's OK if it's bare-bones here. Structure over looks.

2. Port components to Django
3. Create form widgets
4. Features removed? Update help. Update landing page.
5. Update all architecture docs.

### Removal steps

These are sub-steps of the implementation stage.

1. Remove `frontend/`
2. Remove frontend Docker builds
3. Remove reverse proxy
4. Remove frontend stuff from GitHub actions and CircleCI config
5. Remove frontend from render.com blueprint
6. Remove WebSocket API
7. Remove REST API

## Testing

1. Test and compare the two implementations.
2. Perform thorough test of billing logic.
3. Security audit. Check CSPs and other gotchas. Update security docs.
4. Good enough? Continue. Broken? Go back to Analysis
5. User tests.

## Deployment

1. Deploy on render.com. Test thoroughly.
2. Security audit for Projectify on render.com

## Acceptance test

1. Perform user tests.
2. Gather user feedback.
3. Understand if this was a success.

# Description of present Projectify

We will identify all landmarks and features present on the main project
dashboard them if we migrate to using backend only

## Side navigation

The side navigation has the following features:

- The currently active project and workspace can be selected.
- A context menu allows them to access workspace settings and the workspace
  archive, and make the side navigation small (_minimize sidebar_)
- Projects can be archived, and their names changed, using the project
  **ellipsis** menu.
- New projects can be created using the **Create new project** button.
- Using the side navigation, users can filter the currently visible project's
  tasks by team members and labels.
- Team members and labels can be filtered by name.
- New labels can be created from the **Filter labels** section.
- Existing labels can be updated from the **Filter labels** section.
- The last active project for a workspace is stored in the browser's local
  storage
- The side navigation minimize state is stored in the browser's local storage
- The three sections, **Projects**, **Team member**, and **Filter labels**
  expanded state is stored in the browser's local storage.

## Sections and tasks

The project's main view shows all sections and tasks within a project.

- A search allows users to filter tasks by name within a project.
- All sections within the project are shown, and their names can be edited
- Sections can be minimized, meaning that their tasks are hidden. The section's
  hidden state is stored in the browser local storage.
- A **Add task** button allows users to add tasks
- A section context menu offers the following functions:
  - Collapse section
  - Switch with next/previous section
  - Edit section title
  - Delete section (irreversible)
- Within a section, each task is listed.
- A task has the following visible attributes
  - Task number
  - Task title
  - Task labels (scrollable overflow). Editable from dashboard directly.
  - Sub tasks completion (if sub tasks are present)
  - Assigned user's avatar. Clickable, allows users to assign new user.
  - Up and down arrows allow changing order within section.
  - Context (**Ellipsis**) menu
- The task context menu offers the following functions
  - Open task
  - Move to section (opens a sub menu with all sections in the project)
  - Move to top/bottom
  - Copy link
  - Delete task
- A floating **Add section** button allows adding more sections to the
  currently active project.

## Task

Once a task is opened, the following features are present:

- Title, assignee, Labels, Due date, description and sub task status are
  visible
- Breadcrumbs show position within workspace
- Edit button allows user to go to task update screen
- Sub tasks section shows sub task progress, allows editing each sub tasks
  title and checking off their _done_ status.

## Modal views

Features that are not accessible from a separate page but are somehow overlaid
or otherwise only usable from the dashboard or task view are:

- Create and update tasks
- Assigning labels and users in project dashboard or task view
- Moving task to new section in project dashboard
- Various creation/deletion/archival confirmation screens accessible from
  dashboard or task:
  - Add new section
  - Add new project
  - Archive project
  - Delete task
  - Rename project
  - Rename section
  - Restore project
- Context menus:
  - User profile context menu (logout/edit profile)
  - Workspace context menu (select the workspace)
  - Side navigation context menu (workspace settings, archive, minimize
    sidebar)
  - Section context menu (edit/delete/change order)
  - Task context menu (described in detail above)
  - Task label assignment (dashboard and task view)
  - Task user assignment (dashboard and task view)
- Mobile navigation overlay (dashboard, task, and other views)

## Migrating modal views

- Add/Create/Update/Archive modals can all be made into separate pages
- Logout, edit profile - make regular links for now
- Workspace settings, archive - make regular links
- Minimize sidebar: Consider removing
- Task context menu:
  - Open task: Remove
  - Move to section: Better to solve this through introducing the _bulk edit_
    feature planned previously, need a top bar for this
  - Move to top/bottom: Either remove or add bulk edit
  - Copy link: Remove
  - Delete task: Replace _bulk edit_
- Section context menu:
  - Ordering sections can be solved by adding up/down buttons.
  - Collapse section: Remove
  - Edit section title: Add pencil icon thing to section instead.
  - Delete section: This should be on its own page. Perhaps we can have a new
    page for editing project information on which sections can be deleted
- Assign label context menu:
  - Make this a `<select multiple>` HTML element. Consider removing from
    dashboard or replacing with corresponding bulk edit.
- Assign user context menu:
  - Make this a `<select>` as well. Consider removing from dashboard or replace
    with corresponding bulk edit.

## Other interactive features

- Keyboard shortcuts
- Live label/user search

## Migrating other interactive features:

- Keyboard shortcuts: Maybe https://htmx.org/examples/keyboard-shortcuts/
- Label search: Either replace with `Alpine.js`, or remove for now
- User search: Either replace with `Alpine.js`, or remove for now

# Work log

Here's is my work log for this project.

## 2024-11-25

I created a project detail view showing the sections and tasks in a project.
It was very easy to make using the Django `generic.detail.DetailView`. The
template naming is somewhat implicit, and the template is automatically
picked up from `workspace/project_detail.html` inside the
`projectify/workspace/templates` directory.

The URL is temporary for now:

```
workspace/project/<uuid>/view
```

It was pleasant to work with Django, there even is a debug toolbar which I have
added a long time ago for admin panel debugging.

## 2024-11-26

I would like to see if Tailwind works with Django. I'm following the
instructions here:

https://django-tailwind.readthedocs.io/en/latest/installation.html

Result: It is integrated into the backend flake build process (after a lot of
experimentation and various Nix path issues)

## 2024-11-27

I tested out `django-htmx`.

https://django-htmx.readthedocs.io/en/latest/installation.html

It was very easy to add.

There was an issue with tailwind not recognizing the templates. It was solved
by correcting the `contents` variable and give it the right glob to scan for
templates in Projectify. It was a bit confusing to correct since it uses
a relative path from within `projectify/theme/static_src`.

With `django-htmx` I now have sections where tasks can be moved up or down,
and only the contents of the section are replaced. Even better: It still
works with JavaScript turned off, in which case it moves tasks and then reloads the
whole page.

## 2024-11-29

Today I will try `django-components`:

https://github.com/EmilStenstrom/django-components
