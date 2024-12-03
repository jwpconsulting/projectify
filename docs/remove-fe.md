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

I created a project detail view showing the sections and tasks in a project. It
was very easy to make using the Django `generic.detail.DetailView`. The
template naming is somewhat implicit, and the template is automatically picked
up from `workspace/project_detail.html` inside the
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
templates in Projectify. It was a bit confusing to correct since it uses a
relative path from within `projectify/theme/static_src`.

With `django-htmx` I now have sections where tasks can be moved up or down, and
only the contents of the section are replaced. Even better: It still works with
JavaScript turned off, in which case it moves tasks and then reloads the whole
page.

## 2024-11-29

Today I will try `django-components`:

https://github.com/EmilStenstrom/django-components

I find that a large part of frontend components props exist to configure
behavior, not style. It might be possible to re-implement components in the
backend and only add a few style props here and there. It might also be a good
opportunity to simplify the styling in general.

`django-components` seems very complex, and could almost be too much for our
purposes.

Let's consider for a second what the alternatives to migrating everything to
Django are:

### Keep SvelteKit and Django architecture

Doesn't change anything. Initial page loads are slow. Maintaining two different
applications is too much for a single developer.

### Migrate everything to be in SvelteKit

The Django ORM alone, and all the security stuff in it make Django worth it
even if just used for a backend. Using SvelteKit to take over the backend part
would not only mean having to re-implement well-tested business logic, it would
also mean compromising on security and quality.

### Migrate everything to a completely different framework/language/library

Why not re-implement everything and make it a slick single binary Go app? Sure,
but again, Django is incredibly powerful when it comes to database-centric
web-apps. Yes, I might also just use Rails or Laravel, but given that I haven't
used Rails in a long time, and don't know Laravel, these aren't good options
either. Go is a great programming language and the fact that it's so simple
would allow me to focus on the "important bits", like making an app that is
useful.

Re-implementing everything using something different means that the work
doubles, since both frontend and backend have to be rewritten. Rewriting the
frontend alone is already a lot of work, and more than that could be
devastating for motivation.

### Fix SSR in SvelteKit

> SvelteKit is a framework for rapidly developing robust, performant web
> applications using Svelte. If you’re coming from React, SvelteKit is similar
> to Next. If you’re coming from Vue, SvelteKit is similar to Nuxt.

I have tried to fix SSR by shifting around stores and so on to eliminate global
state. Yes, it's possible, but I feel like SvelteKit just hasn't been made to
guide you in the right direction and do those things properly from the
beginning. This makes me doubt that SvelteKit is a framework for making web
applications. A framework for making web applications should come with guard
rails that make accidentally embedding global state into your app difficult.

The **State management** [docs](https://svelte.dev/docs/kit/state-management)
were added quite late, and are not helpful after having made a full app. It
makes me question whether there won't be any other surprises.

There are other ideological points where I don't like SvelteKit's direction.
There is a subtle push to use VS Code to write SvelteKit, and despite the
complaints of many users, SvelteKit 1.0 uses square brackets and parentheses to
configure route paths.

The fact that the deploy documentation barely describes the self-hosted use
case also says a lot. I don't like being subtly pushed to using Vercel or
whatever other surprise-1000-USD charge service. Projectify is supposed to be a
self-hostable project management app. Creating all these proprietary lock-ins
doesn't help at all.

Backend/Frontend is an embarrassingly bad pattern for what is essentially a
skin for a database, a glorified excel spreadsheet with some authentication
sprinkled on top (I exaggerate, of course).

In the end all these ideological disagreements also strengthen my desire to
migrate away from SvelteKit. Making Projectify simple, even if that means
giving up a few features, is a net-positive for users and of course the solo
developer working on this project right now.

Django is quite mature, its documentation is translated into many languages,
and in general a good thing to use when trying to create something and opening
it up to the people.

If Projectify is supposed to be maintained for years to come, then going
through the painful process of a rewrite is a one-time thing, and everything
good after that will be a gift that keeps on giving.

## 2024-12-03

Today I will try `Alpine.js`.

https://alpinejs.dev/start-here

I copied the unified JavaScript file from
https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js

Then, I've tried adding a label search that only renders when `Alpine.js` has
loaded using the docs at
https://alpinejs.dev/start-here#building-a-search-input

Using `:class`, I can make a search form that is only shown when Alpine loads.
See https://alpinejs.dev/directives/bind#class-object-syntax

Having interactive search is pretty nice, it might allow taking over the user
and label filter from the SPA.
