"""Workspace views."""
from rest_framework import (
    parsers,
    response,
    views,
)


class ProfilePictureUploadView(views.APIView):
    """View that allows uploading a profile picture."""

    parser_classes = (parsers.MultiPartParser,)

    def post(self, request, format=None):
        """Handle POST."""
        file_obj = request.data["file"]
        request.user.profile_picture = file_obj
        request.user.save()
        return response.Response(status=204)
