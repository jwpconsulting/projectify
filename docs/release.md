---
title: Release checklist
author: Justus
date: 2026-04-13
---

<!--
SPDX-FileCopyrightText: 2026 JWP Consulting GK

SPDX-License-Identifier: AGPL-3.0-or-later
-->

1. Update release information in `CHANGELOG.md`.
2. Run `bin/prepare-release`. This does the following:
  1. Update the Projectify Python package version with `uv version`
  2. Make a new git commit with the files `pyproject.toml`, `uv.lock`, and
     `CHANGELOG.md`.
  3. Create a new git tag with today's date with leading 0's removed. Example:
     **2026-01-01** becomes `2026.1.1`.
3. Run `git push` and `git push --tags`:
   ```bash
   git push --set-upstream origin $(git rev-parse --abbrev-ref HEAD) &&
     git push --tags
   ```
4. Prepare and merge and **pull request** with the single commit from **2.**.
5. Create a new **PyPI release**: Switch to the latest `origin/main` commit and run `uv build` to build a new build archive in `dist/`.
   Run `uv publish --token $(uv auth token upload.pypi.org)` to upload all
   releases in `dist/`:
   ```bash
   git fetch origin && git checkout origin/main
   # Clean up dist directory
   rm dist/*.{whl,tar.gz}
   # Delete virtual environment
   rm -r .venv/
   uv sync && uv build && uv publish --token $(uv auth token upload.pypi.org)
   ```
6. Create **new release** on GitHub: <https://github.com/jwpconsulting/projectify/releases/new>
  1. Under **Select tag** select the tag that you've just created. Example:
     `2026.4.13`
  2. Under **Release title** enter the tag name. Example: **2026-4-13**
  3. **Release notes**: Copy the notes from the `CHANGELOG.md` file.
  4. Make sure **Set as the latest release** is active.
  5. Press **Publish release**
7. Prepare a new release **blog post** on <https://www.projectifyapp.com/admin/blog/post/add/>.
  1. **Blog post title**: Enter **New Projectify release 2026.4.13**, replace
     **2026.4.13** with your release tag.
  2. **Blog post author**: Enter your name
  3. **Blog post slug**: Enter `projectify-release-2026-4-13` and replace
     `2026-4-13` with the hyphenated release tag.
  4. **Content**: Write the release post header and copy the release notes
     below that.

# Example GitHub release

Example GitHub release:

<https://github.com/jwpconsulting/projectify/releases/tag/2026.4.13>

# Example release post

Example Projectify release post:

<https://www.projectifyapp.com/blog/projectify-release-2026-4-13/>

```
New Projectify release 2026.4.13

By Justus Perlwitz
April 13, 2026

Here's what's new for Projectify since the last development log on 2026-04-06.

The newest release version is 2026.4.13. Please update Projectify if you're self-hosting. If you use Projectify on www.projectifyapp.com, you're automatically using the newest version.

You can also find the newest release here:

https://github.com/jwpconsulting/projectify/releases/tag/2026.4.13
Enhancement

    Update general security information to reflect the Hetzner and Lettermint migration
    Update privacy policy and limit the extent of collected information (that Projectify never collected to begin with)
    Update list of data processers to reflect that www.projectifyapp.com uses Hetzner and Lettermint
    Add convenient links to blog post editor on administration page for staff users.

Fixed

    Fix blog existing posts not rendering correctly in Trix editor.

Internal

    Switch from mailgun specific email configuration to generic SMTP-based email specification
    Allow changing the default sender email address with the DEFAULT_FROM_EMAIL credentials variable. See docs/django-configuration.md
    Fix pgbackrest timers in the Ansible systemd configuration

Security

    Update Django
    Update cryptography
```

# Example PyPI release

Here's an example PyPI release:

<https://pypi.org/project/projectify-app/2026.4.13/>
