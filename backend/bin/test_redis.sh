#!/bin/sh
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023 JWP Consulting GK
set -e
poetry run pytest \
    -x \
    --pdb \
    --ds=projectify.settings.test \
    --dc=TestRedis \
    "workspace/test/test_consumers.py"
