#!/usr/bin/env bash
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023,2026 JWP Consulting GK
# Note:
# This script prefixes commands with `uv run` so that you can just run
# `bin/format.sh`
set -e
OK=1

if ! uv run ruff format .; then
    echo "Ruff format encountered a problem. Continuing."
    OK=0
fi

if ! uv run ruff check --fix .; then
    echo "Ruff check encountered a problem. Continuing."
    OK=0
fi

if ! uv run djlint --reformat .; then
    echo "djlint --reformat encountered a problem. Continuing."
    OK=0
fi

if [[ OK -ne 1 ]]; then
    echo "Couldn't format files correctly."
    exit 1
fi
