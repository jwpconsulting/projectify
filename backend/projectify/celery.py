# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2021, 2023 JWP Consulting GK
"""Celery app."""

from celery import Celery

import configurations

configurations.setup()  # type: ignore

app = Celery("proj")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
