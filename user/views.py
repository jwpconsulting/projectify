"""User views."""
from typing import (
    Optional,
    cast,
)

from django.db import models as django_models

from rest_framework import (
    generics,
    parsers,
    request,
    response,
    views,
)

from . import (
    models,
    serializers,
)


class ProfilePictureUploadView(views.APIView):
    """View that allows uploading a profile picture."""

    parser_classes = (parsers.MultiPartParser,)

    def post(
        self, request: request.Request, format: Optional[str] = None
    ) -> response.Response:
        """Handle POST."""
        file_obj = request.data["file"]
        user = cast(models.User, request.user)
        user.profile_picture = file_obj
        user.save()
        return response.Response(status=204)


class UserRetrieve(
    generics.RetrieveAPIView[
        models.User,
        django_models.QuerySet[models.User],
        serializers.UserSerializer,
    ]
):
    """Retrieve user."""

    serializer_class = serializers.UserSerializer

    def get_object(self) -> models.User:
        """Return current user."""
        # This can only ever be AbstractBaseUser-ish because this endpoint is
        # only accessible after logging in
        user = cast(models.User, self.request.user)
        return user
