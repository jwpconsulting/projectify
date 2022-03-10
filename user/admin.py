"""User app model admins."""
from django.contrib import (
    admin,
)

from . import (
    models,
)


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    """User admin."""


@admin.register(models.UserInvite)
class UserInviteAdmin(admin.ModelAdmin):
    """User invite admin."""
