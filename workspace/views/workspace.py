"""Workspace CRUD views."""
import uuid
from typing import (
    Optional,
)

from django.db.models import (
    Prefetch,
)
from django.shortcuts import (
    get_object_or_404,
)

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
class WorkspaceList(
    generics.ListAPIView[
        models.Workspace,
        models.WorkspaceQuerySet,
        serializers.WorkspaceBaseSerializer,
    ]
):
    """List all workspaces for a user."""

    queryset = models.Workspace.objects.all()
    serializer_class = serializers.WorkspaceBaseSerializer

    def get_queryset(self) -> models.WorkspaceQuerySet:
        """Filter by user."""
        user = self.request.user
        return self.queryset.get_for_user(user)


class WorkspaceRetrieve(
    generics.RetrieveAPIView[
        models.Workspace,
        models.WorkspaceQuerySet,
        serializers.WorkspaceSerializer,
    ]
):
    """Workspace retrieve view."""

    queryset = models.Workspace.objects.prefetch_related(
        "label_set",
    ).prefetch_related(
        Prefetch(
            "workspaceboard_set",
            queryset=models.WorkspaceBoard.objects.filter_by_archived(False),
        ),
        Prefetch(
            "workspaceuser_set",
            queryset=models.WorkspaceUser.objects.select_related(
                "user",
            ),
        ),
    )
    serializer_class = serializers.WorkspaceSerializer

    def get_object(self) -> models.Workspace:
        """Return queryset with authenticated user in mind."""
        user = self.request.user
        qs = self.get_queryset()
        qs = qs.filter_for_user_and_uuid(
            user,
            self.kwargs["workspace_uuid"],
        )
        workspace: models.Workspace = get_object_or_404(qs)
        return workspace


# Update
class WorkspacePictureUploadView(views.APIView):
    """View that allows uploading a profile picture."""

    parser_classes = (parsers.MultiPartParser,)

    def post(
        self,
        request: request.Request,
        uuid: uuid.UUID,
        format: Optional[str] = None,
    ) -> response.Response:
        """Handle POST."""
        user = request.user
        file_obj = request.data["file"]
        qs = models.Workspace.objects.filter_for_user_and_uuid(
            user,
            uuid,
        )
        workspace = get_object_or_404(qs)
        workspace.picture = file_obj
        workspace.save()
        return response.Response(status=204)


# Delete
