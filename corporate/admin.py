"""Corporate admin."""
from django.contrib import (
    admin,
)

from . import (
    models,
)


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    """Customer Admin."""
