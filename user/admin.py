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
