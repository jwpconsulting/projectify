#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023, 2026 JWP Consulting GK
"""Configuration for Gunicorn to use with Projectify application."""

import os

wsgi_app = "projectify.wsgi"

# Refer to
# https://docs.gunicorn.org/en/stable/configure.html#configuration-file
if "PORT" in os.environ:
    bind = f"0.0.0.0:{os.environ['PORT']}"
elif "SOCKET" in os.environ:
    bind = f"unix:{os.environ['SOCKET']}"
else:
    raise ValueError("Must specify PORT or SOCKET environment variable")

# TODO understand how many workers to configure

logconfig = "gunicorn-error.log"
