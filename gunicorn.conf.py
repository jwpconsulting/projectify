#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023 JWP Consulting GK
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
