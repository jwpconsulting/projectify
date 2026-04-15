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
3. Run `git push` and `git push --tags`
4. Prepare and merge and **pull request** with the single commit from **2.**.
5. Create **new release** on GitHub: <https://github.com/jwpconsulting/projectify/releases/new>
  1. Under **Select tag** select the tag that you've just created. Example:
     `2026.4.13`
  2. Under **Release title** enter the tag name. Example: **2026-4-13**
  3. **Release notes**: Copy the notes from the `CHANGELOG.md` file.
  4. Make sure **Set as the latest release** is active.
  5. Press **Publish release**
6. Prepare a new release **blog post**.
  1. **Blog post title**: Enter **New Projectify release 2026.4.13**, replace
     **2026.4.13** with your release tag.
  2. **Blog post author**: Enter your name
  3. **Blog post slug**: Enter `projectify-release-2026-4-13` and replace
     `2026-4-13` with the hyphenated release tag.
  4. **Content**: Write the release post header and copy the release notes
     below that.
7. Create a new **PyPI release**:
    1. Run `uv build` to build a new build archive in `dist/`.
    2. Run `uv publish --token (uv auth token upload.pypi.org)` to upload all
       releases in `dist/`.

Example GitHub release: <https://github.com/jwpconsulting/projectify/releases/tag/2026.4.13>

Example Projectify release post: <https://www.projectifyapp.com/blog/projectify-release-2026-4-13/>

Example PyPI release: <https://pypi.org/project/projectify-app/2026.4.13/>
