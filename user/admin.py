# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Copyright (C) 2021, 2022, 2023 JWP Consulting GK
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
"""User app model admins."""
from django.contrib import (
    admin,
)

from . import (
    models,
)


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin[models.User]):
    """User admin."""

    list_filter = ("is_active", "is_staff", "is_superuser")
    list_display = (
        "email",
        "is_active",
        "is_staff",
        "is_superuser",
        "last_login",
    )


@admin.register(models.UserInvite)
class UserInviteAdmin(admin.ModelAdmin[models.UserInvite]):
    """User invite admin."""
