#!/usr/bin/env bash
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023,2026 JWP Consulting GK
# Test collecting static
# Run within uv shell, nix shell, or similar
set -e
export DJANGO_SETTINGS_MODULE="projectify.settings.test"
export DJANGO_CONFIGURATION="Test"
uv run ./manage.py collectstatic --noinput
