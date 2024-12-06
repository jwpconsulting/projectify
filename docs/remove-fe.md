---
title: SvelteKit Frontend removal plan
---

<!--
SPDX-FileCopyrightText: 2024 JWP Consulting GK

SPDX-License-Identifier: AGPL-3.0-or-later
-->

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

- [x] Test out HTMX. Thoroughly. Make sure you are comfortable.
- [x] Take inventory of all frontend pages
- [x] Identify remaining risks
- [x] Determine acceptance criteria.
- [x] Consider alternatives.
- [x] Understand if Tailwind can be used with Django
- [x] Find out way to use something like frontend components in Django.

### Alternatives

The following alternatives to a full rewrite were identified and discussed:

- Change nothing
- Migrate the backend from Django to SvelteKit
- Migrate to completely different framework/language/library
- Fix SSR implementation in SvelteKit

Out of the above, all were deemed as worse options than the current plan. The
only alternative with some merit was to fix the SSR implementation in
SvelteKit. It would bring short term relief, but not eliminate any of the
additional concerns regarding architecture bloat, performance, and dependency
bloat.

## Planning

Subject to change.

- [x] Plan base template structure
- [x] Write out which templates need to be created.
- [ ] Write out which views need to be created.
- [ ] Write out which forms need to be created. See how DRF serializers can be
      turned into forms.
- [ ] Identify all JavaScript only/frontend only functions that need to be
      recreated in Django
- [ ] Identify form widget templates required

## Implementation

Subject to change.

- [ ] Create views, templates and forms in tandem. Write test cases as you go.
      It's OK if it's bare-bones here. Structure over looks.
- [ ] Port components to Django
- [ ] Create form widgets
- [ ] Features removed? Update help. Update landing page.
- [ ] Update all architecture docs.

### Removal steps

These are sub-steps of the implementation stage.

- [ ] Remove `frontend/`
- [ ] Remove frontend Docker builds
- [ ] Remove reverse proxy
- [ ] Remove frontend stuff from GitHub actions and CircleCI config
- [ ] Remove frontend from render.com blueprint
- [ ] Remove WebSocket API
- [ ] Remove REST API

## Testing

- [ ] Test and compare the two implementations.
- [ ] Perform thorough test of billing logic.
- [ ] Security audit. Check CSPs and other gotchas. Update security docs.
- [ ] Good enough? Continue. Broken? Go back to Analysis
- [ ] User tests.

## Deployment

- [ ] Deploy on render.com. Test thoroughly.
- [ ] Security audit for Projectify on render.com

## Acceptance test

An acceptance test shall be performed to ensure that the frontend rewrite went
as planned, and to identify any fixes necessary.

- [ ] Perform user tests.
- [ ] Gather user feedback.
- [ ] Understand if this was a success.

### Acceptance criteria:

The following functional requirements shall be fulfilled and verified during
the acceptance test:

- Email confirmation flow works
- Onboarding works: Ensure that users go through onboarding if no workspace
  exists
- Billing with Stripe can be used (subscribe, cancel, change)
- New projects can be created, updated and archived
- Tasks can be created
- Sub task management works
- Task re-ordering works
- Project section creation and ordering works
- Workspaces can be managed
- Team member management works
- Password change flow works
- Email address change flow works

To be acceptable, a new frontend would have the following non-functional
requirements:

- [ ] Landing page load with < 500 kB transferred, finishes in 1000 ms
- [ ] PageSpeed Insights shall not deteriorate by more than 5 points for both
      mobile and desktop

Regarding security:

- [ ] Absolutely no new CSP, Clickjacking, or `iframe`-related vulnerability
      shall be introduced.
- [ ] Absolutely no new XSS or SQL injection vulnerability shall be introduced.
- [ ] CSRF checking shall be increasingly strict and non-cookie based in the
      best case.
- [ ] The django backend, embedded in an application server, shall interface
      with the web in a secure manner.
- [ ] Any redirect mechanism shall not impact user privacy (especially HTTPS
      redirects)
- [ ] Referrer-related privacy shall improve
- [ ] Any caching mechanisms shall not expose user information.

Regarding the application and network architecture

- [ ] The complexity of the current deployment on Render.com shall not be
      increased.
- [ ] All of the frontend-specific API endpoints shall be removed.

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
