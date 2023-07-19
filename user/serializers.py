"""User app serializers."""
from typing import (
    Optional,
)

from rest_framework import (
    serializers,
)

from projectify import (
    utils,
)

from . import (
    models,
)


class UserSerializer(serializers.ModelSerializer[models.User]):
    """User serializer."""

    profile_picture = serializers.SerializerMethodField()

    def get_profile_picture(self, obj: models.User) -> Optional[str]:
        """Return profile picture."""
        return utils.crop_image(obj.profile_picture, 100, 100)

    class Meta:
        """Meta."""

        model = models.User
        fields = (
            "email",
            "full_name",
            "profile_picture",
        )
