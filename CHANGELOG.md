<!--
SPDX-FileCopyrightText: 2024-2026 JWP Consulting GK

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Changelog

## Unreleased

### Enhancement

- Simplify new/edit task experience. Extract the task title from the
  description.
- Place task search in top to save space

### Breaking

- Remove task labels
- Remove manual task ordering
- Remove project sections. Projects now directly contain tasks.

### Accessibility

- Fix "http://localhost:8100" anchor tag on landing page

### Internal

- Make it easier to run Projectify locally by feature-gating the following
features:
  - Log in with GitHub
  - Log in with Google
  - Stripe billing including the billing and quota pages in the workspace
    settings. This also disables quota checking.
- Update vulture and regex package
- Test Projectify compabilitity with Python 3.14
- Make all workspace app models readonly in the Projectify Django admin.
- Remove trailing "magic" commas with Ruff. This makes the code base shorter.
- Fix inconsistencies in shell scripts (Thanks shellcheck!)
- Remove SubTask model from workspace app.
- Remove chat messages. Projectify hasn't supported chat messages in a while.
- Build Trix from scratch, update Trix version
- Update django debug toolbar 4.3.0 -> 6.3.0

### Security

- Forbid `<object>` tags by setting the `object-src` CSP to `none`.
- Update python-dotenv

## 2026.4.15

### Enhancement

- Add quick add task field at the bottom of each section
- Show tasks in project dashboard on large screens
- Improve query count by caching permission validations
- Speed up section minimizing
- Speed up task action menu hiding

### Internal

- Update `bin/prepare-release` script to commit the changelog in `CHANGELOG.md`
  as well.
- Show draft blog posts
- Clean up unused tailwind colors
- Vendor in newer version of HTMX and create build script
- Refactor project and task detail templates to make use of Django template partials
- Remove alpine.js

### Documentation

- Improve styleguide at `docs/styleguide.md`.
- Document how to rebuild HTMX in `docs/frontend-scripting.md`.

### Security

- Update Pillow and Pytest
- Narrow down CSP configuration and configure HTMX correctly to support
`{{ csp_nonce }}`

### Documentation

- Add release preparation guide in `docs/release.md`.

## 2026.4.13

### Enhancement

- Update general security information to reflect the Hetzner and Lettermint
  migration
- Update privacy policy and limit the extent of collected information (that
  Projectify never collected to begin with)
- Update list of data processers to reflect that www.projectifyapp.com uses
  Hetzner and Lettermint
- Add convenient links to blog post editor on administration page for staff
  users.

### Fixed

- Fix blog existing posts not rendering correctly in Trix editor.

### Internal

- Switch from mailgun specific email configuration to generic SMTP-based email
  specification
- Allow changing the default sender email address with the `DEFAULT_FROM_EMAIL`
  credentials variable. See `docs/django-configuration.md`
- Fix pgbackrest timers in the Ansible systemd configurationjuk

### Security

- Update Django
- Update cryptography

## 2026.4.7

### Enhancement

- Add rich text editor to task description
- Users can now skip onboarding
- Fold solutions pages and pricing page into landing page

### Internal

- Add daily page statistics counter app in `projectify/stats`
- Migrate from Render.com to Hetzner
- Remove Cloudinary dependency
- Remove Whitenoise
- Use `django-minify-compress-staticfiles` to compress static assets
- Integrate `django_sendfile` and serve media file directly
- Refactor and improve `RichTextField` sanitization

## 2026.3.29

Add `projectify-demo` demo command.

## 2026.3.28

### Enhancement

- Remove SvelteKit

## 2025.12.4

### Security

- Update vulnerable dependencies

## 2025.7.10

### Fixed

- Update vulnerable Pillow dependency

## 2025.5.5

### Fixed

- Updated vulnerable dependencies in frontend and backend

### Internal

- Continue frontend rewrite in Django

## 2025.5.6

### Fixed

- Updated vulnerable dependencies in frontend and backend

## 2025.3.6

### Fixed

- Updated outdated dependencies in frontend and backend

### Internal

- Started frontend rewrite in Django

## 2024.8.20

### Fixed

- Internal ordering of tasks was inverted. This prevented users from properly
moving tasks to the top/bottom.

## 2024.8.17

### Changed

- Change frontend `.env.template` file to assume all backend requests are
  proxied through vite server.

### Fixed

- Fix label creation failing because of missing $currentWorkspace
- Fix missing general validation message when creating and updating labels
- Fix outdated Twisted version to 24.7.0
- Fix outdated Django version to 5.1
