#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Copyright (C) 2023 JWP Consulting GK
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""Configuration for Gunicorn to use with Projectify application."""

import os

wsgi_app = "projectify.asgi"

# Refer to
# https://docs.gunicorn.org/en/stable/configure.html#configuration-file
bind = f"0.0.0.0:{os.environ['PORT']}"

# The docs recommend:
# import multiprocessing
# workers = multiprocessing.cpu_count() * 2 + 1
workers = 1
worker_class = "uvicorn.workers.UvicornWorker"

logconfig = "gunicorn-error.log"
