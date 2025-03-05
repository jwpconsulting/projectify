---
title: Frontend replacement Django templates
---

<!--
SPDX-FileCopyrightText: 2024 JWP Consulting GK

SPDX-License-Identifier: AGPL-3.0-or-later
-->

Refer to `docs/remove-fe-pages.md` for an overview of all pages in the current
SvelteKit frontend.

# Base templates

The following base templates shall be created:

- `base.html`: Base template for all frontend pages
- `workspace/dashboard_base.html`: Base template for all workspace pages found
  in the `docs/remove-fe-pages.md` **Platform** section
- `workspace/onboarding_base.html`: Base template for all onboarding pages
  found in the `docs/remove-fe-pages.md` **Onboarding** section
- `storefront/storefront_base.html`: A new template contained in a new project
  application created to serve all of the `docs/remove-fe-pages.md` storefront pages.
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
