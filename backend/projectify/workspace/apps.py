# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2021, 2022, 2023 JWP Consulting GK
"""Workspace app configs."""

from django.apps import (
    AppConfig,
)


class WorkspaceConfig(AppConfig):
    """Workspace AppConfig."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "projectify.workspace"
