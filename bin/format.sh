#!/usr/bin/env bash
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023,2026 JWP Consulting GK
# Note:
# This script prefixes commands with `uv run` so that you can just run
# `bin/format.sh`
set -e
uv run ruff format .
uv run ruff check --fix .
uv run djlint --reformat .
