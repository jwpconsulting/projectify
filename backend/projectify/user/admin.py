# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2021, 2022, 2023 JWP Consulting GK
"""User app model admins."""

from typing import Optional

from django.contrib import (
    admin,
)
from django.http.request import HttpRequest
from django.utils.translation import gettext_lazy as _

from projectify.user.models.user import User
from projectify.user.models.user_invite import UserInvite


@admin.register(User)
class UserAdmin(admin.ModelAdmin[User]):
    """User admin."""

    list_filter = ("is_active", "is_staff", "is_superuser")
    list_display = (
        "__str__",
        "is_active",
        "is_staff",
        "is_superuser",
        "last_login",
    )
    search_fields = (
        "email",
        "preferred_name",
    )
    search_help_text = _("You can search by email and preferred name")


@admin.register(UserInvite)
class UserInviteAdmin(admin.ModelAdmin[UserInvite]):
    """User invite admin."""

    list_filter = ("redeemed",)
    list_display = (
        "email",
        "redeemed",
    )

    def has_change_permission(
        self, request: HttpRequest, obj: Optional[UserInvite] = None
    ) -> bool:
        """Forbid anyone from changing this."""
        del request
        del obj
        return False
