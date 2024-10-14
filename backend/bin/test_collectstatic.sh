#!/usr/bin/env sh
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023 JWP Consulting GK
set -e
export DJANGO_SETTINGS_MODULE=projectify.settings.test
export TEST_STATICFILES_STORAGE=
poetry run ./manage.py collectstatic --noinput
