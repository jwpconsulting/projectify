"""User app user model views."""
from typing import (
    Optional,
)

from django.db import models as django_models

from rest_framework import (
    generics,
    parsers,
    request,
    response,
    views,
)

from .. import (
    models,
    serializers,
)


# Create
# Read
class UserRead(
    generics.RetrieveAPIView[
        models.User,
        django_models.QuerySet[models.User],
        serializers.UserSerializer,
    ]
):
    """Read user."""

    serializer_class = serializers.UserSerializer

    def get_object(self) -> models.User:
        """Return current user."""
        # This can only ever be AbstractBaseUser-ish because this endpoint is
        # only accessible after logging in
        user = self.request.user
        return user


# Update
# Delete


# RPC
class ProfilePictureUpload(views.APIView):
    """View that allows uploading a profile picture."""

    parser_classes = (parsers.MultiPartParser,)

    def post(
        self, request: request.Request, format: Optional[str] = None
    ) -> response.Response:
        """Handle POST."""
        file_obj = request.data["file"]
        user = request.user
        user.profile_picture = file_obj
        user.save()
        return response.Response(status=204)