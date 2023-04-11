"""Workspace views."""
from django.db.models import (
    Prefetch,
)
from django.shortcuts import (
    get_object_or_404,
)

from rest_framework import (
    generics,
    parsers,
    response,
    views,
)

from . import (
    models,
    serializers,
)


class WorkspacePictureUploadView(views.APIView):
    """View that allows uploading a profile picture."""

    parser_classes = (parsers.MultiPartParser,)

    def post(self, request, uuid, format=None):
        """Handle POST."""
        file_obj = request.data["file"]
        qs = models.Workspace.objects.filter_for_user_and_uuid(
            request.user,
            uuid,
        )
        workspace = get_object_or_404(qs)
        workspace.picture = file_obj
        workspace.save()
        return response.Response(status=204)


class WorkspaceBoardRetrieve(generics.RetrieveAPIView):
    """Workspace board retrieve view."""

    queryset = models.WorkspaceBoard.objects.prefetch_related(
        "workspaceboardsection_set",
        "workspaceboardsection_set__task_set",
        "workspaceboardsection_set__task_set__assignee",
        "workspaceboardsection_set__task_set__assignee__user",
        "workspaceboardsection_set__task_set__labels",
        "workspaceboardsection_set__task_set__subtask_set",
    ).select_related(
        "workspace",
    )
    serializer_class = serializers.WorkspaceBoardDetailSerializer

    def get_object(self):
        """Return queryset with authenticated user in mind."""
        user = self.request.user
        qs = self.get_queryset().filter_for_user_and_uuid(
            user,
            self.kwargs["workspace_board_uuid"],
        )
        workspace_board = get_object_or_404(qs)
        return workspace_board


class WorkspaceBoardSectionRetrieve(generics.RetrieveAPIView):
    """Workspace board retrieve view."""

    queryset = models.WorkspaceBoardSection.objects.prefetch_related(
        "task_set",
        "task_set__assignee",
        "task_set__assignee__user",
        "task_set__labels",
        "task_set__subtask_set",
    ).select_related(
        "workspace_board",
        "workspace_board__workspace",
    )
    serializer_class = serializers.WorkspaceBoardSectionDetailSerializer

    def get_object(self):
        """Return queryset with authenticated user in mind."""
        user = self.request.user
        qs = self.get_queryset().filter_for_user_and_uuid(
            user,
            self.kwargs["workspace_board_section_uuid"],
        )
        workspace_board_section = get_object_or_404(qs)
        return workspace_board_section


class WorkspaceList(generics.ListAPIView):
    """List all workspaces for a user."""

    queryset = models.Workspace.objects.all()
    serializer_class = serializers.WorkspaceBaseSerializer

    def get_queryset(self):
        """Filter by user."""
        return self.queryset.get_for_user(self.request.user)


class WorkspaceRetrieve(generics.RetrieveAPIView):
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

    def get_object(self):
        """Return queryset with authenticated user in mind."""
        user = self.request.user
        qs = self.get_queryset().filter_for_user_and_uuid(
            user,
            self.kwargs["workspace_uuid"],
        )
        workspace = get_object_or_404(qs)
        return workspace


class TaskRetrieve(generics.RetrieveAPIView):
    """Retrieve a task."""

    queryset = (
        models.Task.objects.select_related(
            "workspace_board_section__workspace_board__workspace",
            "assignee",
            "assignee__user",
        )
        .prefetch_related(
            "labels",
            "subtask_set",
        )
        .prefetch_related(
            Prefetch(
                "chatmessage_set",
                queryset=models.ChatMessage.objects.select_related(
                    "author",
                    "author__user",
                ),
            ),
        )
    )
    serializer_class = serializers.TaskDetailSerializer

    def get_object(self):
        """Get object for user and uuid."""
        return (
            self.get_queryset()
            .filter_for_user_and_uuid(
                self.request.user,
                self.kwargs["task_uuid"],
            )
            .get()
        )


class WorkspaceBoardArchivedList(generics.ListAPIView):
    """List archived workspace boards inside a workspace."""

    queryset = models.WorkspaceBoard.objects.filter_by_archived()
    serializer_class = serializers.WorkspaceBoardBaseSerializer

    def get_queryset(self):
        """Get queryset."""
        user = self.request.user
        qs = models.Workspace.objects.filter_for_user_and_uuid(
            user,
            self.kwargs["workspace_uuid"],
        )
        workspace = get_object_or_404(qs)
        return self.queryset.filter_by_workspace(workspace)
