"""Corporate app serializers."""
from rest_framework import (
    serializers,
)

from . import (
    models,
)


class CustomerSerializer(serializers.ModelSerializer):
    """Serializer for customer."""

    class Meta:
        """Meta."""

        model = models.Customer
        fields = (
            "seats",
            "uuid",
            "subscription_status",
        )
