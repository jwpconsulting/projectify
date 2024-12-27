# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2021 JWP Consulting GK
"""User apps."""

from django.apps import AppConfig


class UserConfig(AppConfig):
    """UserConfig class."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "projectify.user"
