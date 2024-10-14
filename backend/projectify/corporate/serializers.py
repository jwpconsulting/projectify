# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023 JWP Consulting GK
"""Corporate app serializers."""

from rest_framework import serializers

from . import models


class CustomerSerializer(serializers.ModelSerializer[models.Customer]):
    """Serializer for customer."""

    class Meta:
        """Meta."""

        model = models.Customer
        fields = (
            "seats",
            "uuid",
            "subscription_status",
        )
        extra_kwargs = {
            "seats": {"required": True},
            "subscription_status": {"required": True},
        }
