"""Corporate admin."""
from django.contrib import (
    admin,
)
from django.utils.translation import gettext_lazy as _

from . import (
    models,
)


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    """Customer Admin."""

    list_display = ("workspace_title", "seats", "subscription_status")
    list_select_related = ("workspace",)
    readonly_fields = (
        "uuid",
        "stripe_customer_id",
    )

    @admin.display(description=_("Workspace title"))
    def workspace_title(self, instance):
        """Return the workspace's title."""
        return instance.workspace.title
