# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2021, 2022, 2023 JWP Consulting GK
"""User app model admins."""

from typing import Optional

from django.contrib import admin
from django.http.request import HttpRequest
from django.utils.translation import gettext_lazy as _

from projectify.lib.admin import ReadOnlyAdmin
from projectify.user.models import (
    PreviousEmailAddress,
    User,
    UserEvent,
    UserInvite,
)


class UserEventAdmin(ReadOnlyAdmin[UserEvent], admin.TabularInline[UserEvent]):
    """Inline admin for UserEvent."""

    model = UserEvent
    extra = 0
    readonly_fields = ("created",)
    fields = ("created", "user_agent", "ip_address")


class PreviousEmailAddressAdmin(
    ReadOnlyAdmin[PreviousEmailAddress],
    admin.TabularInline[PreviousEmailAddress],
):
    """Inline admin for PreviousEmailAddress."""

    model = PreviousEmailAddress
    extra = 0


@admin.register(User)
class UserAdmin(admin.ModelAdmin[User]):
    """User admin."""

    exclude = ("password",)
    readonly_fields = (
        "tos_agreed",
        "privacy_policy_agreed",
        "preferred_name",
        "is_superuser",
        "last_login",
        "activated",
    )
    list_filter = ("is_active", "is_staff", "is_superuser")
    list_display = (
        "__str__",
        "is_staff",
        "is_superuser",
        "created",
        "activated",
        "last_login",
    )
    search_fields = ("email", "preferred_name")
    search_help_text = _("You can search by email and preferred name")
    inlines = [PreviousEmailAddressAdmin, UserEventAdmin]


@admin.register(UserInvite)
class UserInviteAdmin(admin.ModelAdmin[UserInvite]):
    """User invite admin."""

    list_filter = ("redeemed",)
    list_display = ("email", "redeemed")

    def has_change_permission(
        self, request: HttpRequest, obj: Optional[UserInvite] = None
    ) -> bool:
        """Forbid anyone from changing this."""
        del request
        del obj
        return False
