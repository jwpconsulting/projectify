"""Workspace views."""
from django.db.models import (
    Prefetch,
)
from django.shortcuts import (
    get_object_or_404,
)

from rest_framework import (
    generics,
)

from .. import (
    models,
    serializers,
)

# Reexport
# flake8: noqa: F401
from .workspace import *


class WorkspaceBoardRetrieve(
    generics.RetrieveAPIView[
        models.WorkspaceBoard,
        models.WorkspaceBoardQuerySet,
        serializers.WorkspaceBoardDetailSerializer,
    ]
):
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

    def get_object(self) -> models.WorkspaceBoard:
        """Return queryset with authenticated user in mind."""
        user = self.request.user
        qs = self.get_queryset()
        qs = qs.filter_for_user_and_uuid(
            user,
            self.kwargs["workspace_board_uuid"],
        )
        workspace_board: models.WorkspaceBoard = get_object_or_404(qs)
        return workspace_board


class WorkspaceBoardSectionRetrieve(
    generics.RetrieveAPIView[
        models.WorkspaceBoardSection,
        models.WorkspaceBoardSectionQuerySet,
        serializers.WorkspaceBoardSectionDetailSerializer,
    ]
):
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

    def get_object(self) -> models.WorkspaceBoardSection:
        """Return queryset with authenticated user in mind."""
        user = self.request.user
        qs = self.get_queryset()
        qs = qs.filter_for_user_and_uuid(
            user,
            self.kwargs["workspace_board_section_uuid"],
        )
        workspace_board_section: models.WorkspaceBoardSection = (
            get_object_or_404(qs)
        )
        return workspace_board_section


class TaskRetrieve(
    generics.RetrieveAPIView[
        models.Task, models.TaskQuerySet, serializers.TaskDetailSerializer
    ],
):
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

    def get_object(self) -> models.Task:
        """Get object for user and uuid."""
        user = self.request.user
        qs: models.TaskQuerySet = self.get_queryset()
        obj: models.Task = qs.filter_for_user_and_uuid(
            user,
            self.kwargs["task_uuid"],
        ).get()
        return obj


class WorkspaceBoardArchivedList(
    generics.ListAPIView[
        models.WorkspaceBoard,
        models.WorkspaceBoardQuerySet,
        serializers.WorkspaceBoardBaseSerializer,
    ]
):
    """List archived workspace boards inside a workspace."""

    queryset = models.WorkspaceBoard.objects.filter_by_archived()
    serializer_class = serializers.WorkspaceBoardBaseSerializer

    def get_queryset(self) -> models.WorkspaceBoardQuerySet:
        """Get queryset."""
        user = self.request.user
        qs = models.Workspace.objects.filter_for_user_and_uuid(
            user,
            self.kwargs["workspace_uuid"],
        )
        workspace = get_object_or_404(qs)
        return self.queryset.filter_by_workspace(workspace)
