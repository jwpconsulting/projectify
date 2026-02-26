#!/usr/bin/env sh
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023,2026 JWP Consulting GK
# Note:
# Run within a uv shell, nix shell, or similar environment
set -e
ruff format .
ruff check --fix .
djlint --reformat .
