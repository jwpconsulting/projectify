"""Corporate models."""
from django.db import (
    models,
)


class Customer(models.Model):
    """Customer model. One to one linked to workspace."""

    workspace = models.OneToOneField(
        "workspace.Workspace",
        on_delete=models.CASCADE,
    )
