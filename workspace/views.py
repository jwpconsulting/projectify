"""Workspace views."""
from rest_framework import (
    parsers,
    response,
    views,
)

from . import (
    models,
)


class WorkspacePictureUploadView(views.APIView):
    """View that allows uploading a profile picture."""

    parser_classes = (parsers.MultiPartParser,)

    def post(self, request, uuid, format=None):
        """Handle POST."""
        file_obj = request.data["file"]
        workspace = models.Workspace.objects.get_for_user_and_uuid(
            request.user,
            uuid,
        )
        workspace.picture = file_obj
        workspace.save()
        return response.Response(status=204)
