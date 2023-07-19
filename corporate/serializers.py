"""Corporate app serializers."""
from rest_framework import (
    serializers,
)

from . import (
    models,
)


class CustomerSerializer(serializers.ModelSerializer[models.Customer]):
    """Serializer for customer."""

    seats_remaining = serializers.IntegerField(read_only=True)

    class Meta:
        """Meta."""

        model = models.Customer
        fields = (
            "seats",
            "uuid",
            "subscription_status",
            "seats_remaining",
        )
