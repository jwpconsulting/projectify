<!--
SPDX-FileCopyrightText: 2024 JWP Consulting GK

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Projectify

Projectify is a free software project management software that anyone can use,
inspect, customize and distribute according to their needs.

Official instance:
[https://www.projectifyapp.com](https://www.projectifyapp.com).

This repository contains both frontend and backend code.

The frontend uses SvelteKit to run. The backend is implemented in Django.

# Frontend

See `frontend/` subfolder and refer to `README.md` on how to get started
running the Projectify frontend.

Originally merged from `projectify-frontend` repository main branch [served on
GitHub](https://github.com/jwpconsulting/projectify-frontend) using

```
git subtree add -P frontend git@github.com:jwpconsulting/projectify-frontend.git main
```

# Backend

See `backend/` subfolder and refer to `README.md` on how to get started running
and developing the backend code

# Nix

Projectify relies on Nix for various build and run tasks, such as Docker builds
or providing a runtime environment for supervisor.

Getting started with Nix might be challenging, but will be worth it. If you
have Nix, Nix flakes (experimental commands), nix-direnv set up, you can get started with running

```bash
# Of course, please audit the .envrc file first, before you run the
# following:
direnv allow
```

# License

Both frontend and backend code are licensed under the GNU Affero General Public
License Version 3 or later. Some third party dependencies are vendored in and
available under their respective licenses. Please review the license files
contained in the `LICENSES` directory located in the Projectify repository.

See `AUTHORS.txt` file for the list of contributors.

Projectify is a registered trademark by [JWP Consulting
GK](https://www.jwpconsulting.net).
