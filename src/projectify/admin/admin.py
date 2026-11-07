# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2024 JWP Consulting GK
"""Admin configuration for Projectify."""

from django.conf import settings
from django.contrib import admin
from django.utils.translation import gettext_lazy as _


class ProjectifyAdmin(admin.AdminSite):
    """
    Configure Django admin for Projectify.

    Some of the things we like to set:
    - Name
    - Show whether dev environment is used or not

    Sort of like when you want to make sure you run rm -r / on the correct
    SSH console.
    """

    # The header shown in the top nav bar
    site_header = _("Projectify Admin ({})").format(
        settings.SITE_TITLE or "UNKNOWN"
    )
    # Right half of <title>, ... | Projectify Administration
    site_title = site_header
    # Left half of <title> when visiting admin,
    # Index | Projectify Administration
    index_title = _("Index")
