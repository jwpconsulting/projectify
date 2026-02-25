# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2022, 2023 JWP Consulting GK
"""Premail app config."""

from django.apps import AppConfig


class PremailConfig(AppConfig):
    """App config."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "projectify.premail"

    def ready(self) -> None:
        """Populate the email registry."""
        from .registry import populate_registry

        populate_registry()
