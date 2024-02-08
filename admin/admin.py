# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Copyright (C) 2024 JWP Consulting GK
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
"""Admin configuration for Projectify."""
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
    site_header = _("Projectify Administration")
    # Right half of <title>, ... | Projectify Administration
    site_title = _("Projectify Administration")
    # Left half of <title> when visiting admin,
    # Index | Projectify Administration
    index_title = _("Index")
