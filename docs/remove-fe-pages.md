---
title: Frontend pages to be re-implemented in backend
date: 2024-11-29
---

<!--
SPDX-FileCopyrightText: 2024 JWP Consulting GK

SPDX-License-Identifier: AGPL-3.0-or-later
-->

This document describes all pages in the frontend which will be replaced by an
equivalent page in the backend.

<!--
tree src/routes/ -P / -I stories
-->

```
src/routes/
├── assets
├── (onboarding)
│   └── onboarding
│       ├── about-you
│       ├── assign-task
│       │   └── [taskUuid]
│       ├── new-label
│       │   └── [taskUuid]
│       ├── new-project
│       │   └── [workspaceUuid]
│       ├── new-task
│       │   └── [projectUuid]
│       ├── new-workspace
│       └── welcome
├── (platform)
│   ├── dashboard
│   │   ├── project
│   │   │   └── [projectUuid]
│   │   │       └── search
│   │   ├── section
│   │   │   └── [sectionUuid]
│   │   │       └── create-task
│   │   ├── task
│   │   │   └── [taskUuid]
│   │   │       └── update
│   │   └── workspace
│   │       └── [workspaceUuid]
│   │           ├── archive
│   │           └── settings
│   │               ├── billing
│   │               ├── quota
│   │               └── team-members
│   └── user
│       └── profile
│           ├── changed-password
│           ├── change-password
│           └── update-email-address
│               ├── confirm
│               │   └── [token]
│               ├── confirmed
│               └── requested
└── (storefront)
    ├── accessibility
    ├── assets
    ├── contact-us
    ├── credits
    ├── ethicalads
    ├── free-software
    ├── help
    │   └── (page)
    │       ├── basics
    │       ├── billing
    │       ├── filters
    │       ├── keyboard-shortcuts
    │       ├── labels
    │       ├── projects
    │       ├── quota
    │       ├── roles
    │       ├── sections
    │       ├── tasks
    │       ├── team-members
    │       ├── trial
    │       └── workspaces
    ├── pricing
    ├── privacy
    ├── security
    │   ├── disclose
    │   └── general
    ├── solutions
    │   ├── academic
    │   ├── assets
    │   ├── development-teams
    │   ├── personal-use
    │   ├── project-management
    │   ├── remote-work
    │   └── research
    ├── tos
    └── user
        ├── (auth)
        │   ├── confirm-email
        │   │   └── [email]
        │   │       └── [token]
        │   ├── confirm-password-reset
        │   │   └── [email]
        │   │       └── [token]
        │   ├── log-in
        │   ├── request-password-reset
        │   └── sign-up
        ├── log-out
        ├── requested-password-reset
        ├── reset-password
        └── sent-email-confirmation-link
```

We will list off all pages based on the root template used, either

- `onboarding`,
- `storefront`, or
- `platform`

# Storefront

The storefront has many pre-rendered pages and a few pages for user
authentication. The difference between storefront and platform in this regard
is that storefront can be accessed without being logged in, while platform
requires authentication.

## Overview

These are the pre-rendered pages:

- `accessibility`: Uses a Markdown document
- `contact-us`: Uses a Markdown document
- `credits`: Shows frontend packages used, the rest is written in Markdown
- `ethicalads`: This is an exact copy of the landing page.
- `free-software`: Uses a Markdown document
- `help`: Has some structured JavaScript information that we can just render in
  the server for now.
  - `basics`: Markdown
  - `billing`: Markdown
  - `filters`: Markdown
  - `keyboard-shortcuts`: Markdown
  - `labels`: Markdown
  - `projects`: Markdown
  - `quota`: Markdown
  - `roles`: Markdown
  - `sections`: Markdown
  - `tasks`: Markdown
  - `team-members`: Markdown
  - `trial`: Markdown
  - `workspaces`: Markdown
- `pricing`: Very fancy layout, no Markdown.
- `privacy`: Custom `.svelte` files. Can be turned into HTML easily, I assume.
- `security`: Markdown
  - `disclose`: Markdown
  - `general`: Markdown
- `solutions`: Fancy layout, has structured JavaScript information that we can
  copy into the backend.
  - `academic`: Layout rendered based on structured information
  - `development-teams`: Layout rendered based on structured information
  - `personal-use`: Layout rendered based on structured information
  - `project-management`: Layout rendered based on structured information
  - `remote-work`: Layout rendered based on structured information
  - `research`: Layout rendered based on structured information
- `tos`: Custom `.svelte` files. Can be turned into HTML easily, I assume.

## Help pages

A help page for a given topic consists of the following data:

- `src/routes/(platform)/help/$TOPIC/+page.svelte`: The Svelte page
- `message/en/help/$TOPIC.md` Markdown content
- Corresponding entry in `src/messages/en.ts`.

This is how a help page looks like in Svelte:

```svelte
<!-- @component Comment -->
<script lang="ts">
    import { _ } from "svelte-i18n";

    import Layout from "$lib/components/help/Layout.svelte";
    import type { SolutionsHeroContent } from "$lib/types/ui";

    $: heroContent = {
        title: $_("help.$TOPIC.title"),
        text: $_("help.$TOPIC.description"),
    } satisfies SolutionsHeroContent;
</script>

<Layout {heroContent} content={$_("help.$TOPIC.content")} />
```

This is how an entry for `$TOPIC` in `src/messages/en.ts` looks like:

```javascript
// ...
"quota": {
    title: "Workspace quotas",
    description: "Understand workspace resource quotas",
    content: QuotaHelpPage,
},
// ...
```

### Migration

To migrate, we set up the following folder structure and files:

- Create `backend/projectify/help` app
- Create `backend/projectify/help/templates/help/help_list.html` list template
- Create `backend/projectify/help/templates/help/help_detail.html` individual
  help page layout
- Install
  [`Django Markdownify`](https://django-markdownify.readthedocs.io/en/latest/)
- Create list and detail Django class-based view.
- Create URLs for help list and help detail.

The class based view for the help detail should take a look at a help topic
`kwargs`, and pass the correct string to be turned into Markdown in the render
context. We add a simple dict that matches the topic `kwargs` with a lazy
`gettext` translated string. The strings are then pulled out using Django
`gettext`.

The template for the help detail page will somewhat look like this:

```html
{% extends "base.html" %} {% load markdownify %} {{ help_text | markdownify }}
```

Then, for a help page for `$TOPIC`, find the corresponding string in the
message file and add the correct Markdown from the frontend there.

## Solutions

This is how a solutions page `$SOLUTION` looks like:

```svelte
<script lang="ts">
    import { _ } from "svelte-i18n";

    import SolutionsPage from "$lib/components/solutions/SolutionsPage.svelte";
    import type { SolutionsPageContent } from "$lib/types/ui";

    import Picture1 from "../assets/picture1.png?enhanced";
    import Hero$SOLUTION from "../assets/hero-$SOLUTION.png?enhanced";

    $: pageContent = {
        heroContent: {
            title: $_("solutions.$SOLUTION.hero.title"),
            text: $_("solutions.$SOLUTION.hero.text"),
            image: {
                src: Hero$SOLUTION,
                alt: $_("solutions.index.solutions.$SOLUTION.illustration.alt"),
            },
        },
        features: [
            {
                image: {
                    position: "left",
                    src: Picture1,
                    alt: $_(
                        "solutions.$SOLUTION.features.feature-N.illustration.alt",
                    ),
                },
                title: $_("solutions.$SOLUTION.features.feature-N.title"),
                text: $_("solutions.$SOLUTION.features.feature-N.text"),
            },
        ],
    } satisfies SolutionsPageContent;
</script>

<SolutionsPage {pageContent} />
```

We might get by with creating the following:

- Solutions base template
- Individual solutions template
- Solutions index view function
- Make template for hero and individual feature
- Individual solutions view function (for each)

Then, create each individual solutions page:

1. `academic`
2. `development-teams`
3. `personal-use`
4. `project-management`
5. `remote-work`
6. `research`

Copy all assets required by these pages. At some point we might want to add
something for asset optimization like https://pypi.org/project/django-pictures/

## Other storefront pages

The other pages are a combination of Markdown or HTML, so we can use the above
templates string `gettext` trick and load them into `Django-markdownify`.

The landing page is a one-off so we can probably just copy-paste the HTML here.

The user pages are very form-based, something to figure out as we go.

# Onboarding

The onboarding steps are also described in `docs/frontend/onboarding.md`.

We need to implement the following pages:

- _About you_: `/onboarding/about-you`
- _New workspace_: `/onboarding/new-workspace`
- _New project_: `/onboarding/new-project/[workspaceUuid]`
- _New task_: `/onboarding/new-task/[projectUuid]`
- _New label_: `/onboarding/new-label/[taskUuid]`
- _Assign task (confirmation)_: `/onboarding/assign-task/[taskUuid]`

## Migration

These pages are a bit more complex, each one consists of a form with data
validation. We should probably just start working on them and see where we end
up.

# Platform

Platform pages require for the user to be authenticated.

A brief description of the platform pages follows:

- `dashboard`: Redirects to the first workspace and project we find for a
  logged in user
- `dashboard/project/[projectUuid]`: Shows a project. Already made a prototype
  with a bit of HTMX sprinkled on top
- `dashboard/project/[projectUuid]/search`: Show search results for tasks
  searched within a project
- `dashboard/section/[sectionUuid]/create-task`: Create task within section
- `dashboard/task/[taskUuid]`: Show task
- `dashboard/task/[taskUuid]/update`: Update task form
- `dashboard/workspace/[workspaceUuid]`: Redirect to first project within
  workspace
- `dashboard/workspace/[workspaceUuid]/archive`: Show archived projects within
  workspace. Allow user to recover projects.
- `dashboard/workspace/[workspaceUuid]/settings`: Show general workspace
  settings
- `dashboard/workspace/[workspaceUuid]/settings/billing`: Show workspace
  billing settings
- `dashboard/workspace/[workspaceUuid]/settings/quota`: Show remaining quotas
  for workspace entities
- `dashboard/workspace/[workspaceUuid]/settings/team-member`: Add/remove team
  members
- `user/profile`: Update user profile picture and display name
- `user/profile/change-password`: Password change dialog
- `user/profile/changed-password`: Success status page shown when password
  changed successfully.
- `user/profile/update-email-address`: Email address update dialog
- `user/profile/update-email-address/requested`: Shown when email address
  change requested
- `user/profile/update-email-address/confirm/[token]`: Opened in browser to
  confirm new email address
- `user/profile/update-email-address/confirmed`: Success status page shown when
  email address updated successfully.

The above pages are all highly dynamic and do not use content derived from
Markdown files.

# Base templates

The following base templates shall be created:

- `base.html`: Base template for all frontend pages
- `workspace/dashboard_base.html`: Base template for all workspace pages found
  in the above **Platform** section
- `workspace/onboarding_base.html`: Base template for all onboarding pages
  found in the above **Onboarding** section
- `storefront/storefront_base.html`: A new template contained in a new project
  application created to serve all of the above storefront pages.
- `storefront/storefront_hero.html`: Used for all the hero pages

# Storefront templates

Furthermore, to serve all storefront pages, the following templates shall be
created. Written in parentheses is the original format in which the content of
that page is stored in the current SvelteKit frontend. Most of the below pages
use some kind of hero layout.

- `storefront/accessibility.html`: Render **Accessibility** page (Markdown)
- `storefront/contact_us.html`: Render **Contact us** page (Markdown)
- `storefront/credits.html`: Render **Credits** page (partial Markdown)
- `storefront/free-software.html`: Render **Free Software and License
  Information** page (Markdown)
- `storefront/help_index.html`: Renders help index (Structured JSON)
- `storefront/help_detail.html`: Render individual help page (Markdown,
  Structured JSON)
- `storefront/pricing.html`: Show **Pricing** info (Svelte)
- `storefront/privacy.html`: Show **Privacy Policy** (Svelte)
- `storefront/security_general.html`: Show **Security** page (Markdown)
- `storefront/security_disclose.html`: Show **Vulnerability Disclosure Policy**
  (Markdown)
- `storefront/solutions_index.html`: Render **Solutions** index (Structured
  JSON)
- `storefront/solutions_detail.html`: Renders solutions detail (Structured
  JSON)
- `storefront/tos.html`: Show **Terms of service** (Svelte)

Furthermore, these pages shall be created to enable user registration and
authentication:

- `user/confirm_email.html`: Shown when user confirms email address with a
  special token sent to their email address
- `user/confirm_password_reset.html`: Allows user to change their password,
  given they use the right token sent to their email address
- `user/log_in.html`: Log in page
- `user/request_password_reset.html`: Allows user to reset their password by
  entering their email address.
- `user/sign_up.html`: Sign up page
- `user/log_out.html`: Log out success page
- `user/requested_password_reset.html`: Shown when password reset email has
  been sent to a user.
- `user/reset_password.html`: Success page when user password has been reset
- `user/sent_email_confirmation_link.html`: Success page when user has signed
  up and confirmation email was sent to them.

A template for the above pages shall be created:
`user/user_storefront_base.html`.

# Platform templates

These are the base templates that shall be implemented to support rendering the
individual platform pages, as listed in the **Platform** section. Contained
within them are the templates that are built on top of the base templates.

- `workspace/project_base.html`: Used to render project pages
  - `workspace/project_detail.html`: Shows a project
  - `workspace/project_search.html`: Shows task search results within project
- `workspace/workspace_base.html`: Used to render workspace settings
  - `workspace/workspace_archive.html`: Show archived projects
  - `workspace/workspace_settings.html`: Show general settings
  - `workspace/workspace_biling.html`: Show billing settings settings
  - `workspace/workspace_team_members.html`: Show team member settings
- `workspace/task_base.html`: Used to render task pages
  - `workspace/task_create.html`: Task creation view
  - `workspace/task_detail.html`: Show task details
  - `workspace/task_update.html`: Show task update screen
- `user/profile_base.html`: Used to render profile related pages
  - `user/change_password.html`: Password change page
  - `user/changed_password.html`: Password change success page
  - `user/update_email_address.html`: Email address change page
  - `user/update_email_address_request.html`: Email address change requested
    page
  - `user/update_email_address_confirm.html`: Confirm change using token
    received with new email address
  - `user/update_email_address_confirmed.html`: Email address change success
    page

# Error pages

Generic error pages shall be created:

- `404.html`: When something isn't found
- `403.html`: When a page requires users to be authenticated
- `500.html`: When something goes wrong.

# Reusable partial templates

The following partial templates shall be created for inclusion in other
templates. This list might not be complete

- `workspace/include/side_nav.html`: Universal side navigation used in almost
  all dashboard pages
- `workspace/include/navigation`: Dashboard navigation bar
- `include/navigation.html`: Universal navigation bar (except dashboard)
- `include/footer.html`: Universal footer
