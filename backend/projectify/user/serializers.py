# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2022, 2023 JWP Consulting GK
"""User app serializers."""

from typing import Optional, Sequence

from rest_framework import serializers

from projectify import utils

from . import models


class UserSerializer(serializers.ModelSerializer[models.User]):
    """User serializer."""

    profile_picture = serializers.SerializerMethodField()

    def get_profile_picture(self, obj: models.User) -> Optional[str]:
        """Return profile picture."""
        return utils.crop_image(obj.profile_picture, 100, 100)

    class Meta:
        """Meta."""

        model = models.User
        fields: Sequence[str] = (
            "email",
            "preferred_name",
            "profile_picture",
        )
        extra_kwargs = {"preferred_name": {"required": True}}


class LoggedInUserSerializer(UserSerializer):
    """Serialize logged in user."""

    kind = serializers.ChoiceField(
        choices=["authenticated"],
        read_only=True,
        default="authenticated",
    )

    class Meta(UserSerializer.Meta):
        """Copy meta from UserSerializer."""

        fields = (
            "email",
            "kind",
            "preferred_name",
            "profile_picture",
        )


class AnonymousUserSerializer(serializers.Serializer):
    """Serialize anonymous user."""

    kind = serializers.ChoiceField(
        choices=["unauthenticated"],
        required=True,
    )
