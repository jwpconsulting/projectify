"""Corporate factories."""
import factory
from factory import (
    django,
)

from . import (
    models,
)


class CustomerFactory(django.DjangoModelFactory):
    """Customer factory."""

    workspace = factory.SubFactory("workspace.factory.WorkspaceFactory")

    class Meta:
        """Meta."""

        model = models.Customer
