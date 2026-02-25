# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2024 JWP Consulting GK
"""
Projectify app configs.

Contains reference to admin configuration here.
"""

from django.contrib.admin.apps import AdminConfig


class ProjectifyAdminConfig(AdminConfig):
    """Configure Projectify admin site."""

    default_site = "projectify.admin.admin.ProjectifyAdmin"
