#!/usr/bin/env sh
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023 JWP Consulting GK
# Note:
# Run within a poetry, nix, or similar environment
set -e
ruff format .
ruff check --fix .
djlint --reformat .
