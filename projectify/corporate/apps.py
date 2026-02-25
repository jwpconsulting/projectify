# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2022, 2023 JWP Consulting GK
"""Corporate app config."""

from django.apps import AppConfig


class CorporateConfig(AppConfig):
    """App config."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "projectify.corporate"
