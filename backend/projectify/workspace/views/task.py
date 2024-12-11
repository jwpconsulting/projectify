# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023-2024 JWP Consulting GK
"""Task CRUD views."""

from uuid import UUID

from django.utils.translation import gettext_lazy as _

from rest_framework import serializers, status
from rest_framework.exceptions import NotFound
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from projectify.lib.error_schema import DeriveSchema
from projectify.lib.schema import extend_schema
from projectify.workspace.models.section import Section
from projectify.workspace.selectors.section import (
    section_find_for_user_and_uuid,
)
from projectify.workspace.selectors.task import (
    TaskDetailQuerySet,
    task_find_by_task_uuid,
)
from projectify.workspace.serializers.task_detail import (
    TaskCreateSerializer,
    TaskDetailSerializer,
    TaskUpdateSerializer,
)
from projectify.workspace.services.sub_task import ValidatedData
from projectify.workspace.services.task import (
    task_create_nested,
    task_delete,
    task_move_after,
    task_update_nested,
)

from .. import models


def get_object(request: Request, task_uuid: UUID) -> models.Task:
    """Get object for user and uuid."""
    user = request.user
    obj = task_find_by_task_uuid(
        who=user, task_uuid=task_uuid, qs=TaskDetailQuerySet
    )
    if obj is None:
        raise NotFound(
            _("Task with uuid {task_uuid} not found").format(
                task_uuid=task_uuid
            )
        )
    return obj


# Create
class TaskCreate(APIView):
    """Create a task."""

    @extend_schema(
        request=TaskCreateSerializer,
        responses={201: TaskDetailSerializer, 400: DeriveSchema},
    )
    def post(self, request: Request) -> Response:
        """Handle POST."""
        serializer = TaskCreateSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        section: Section = validated_data["section"]

        sub_tasks: ValidatedData
        if "sub_tasks" in validated_data:
            sub_tasks = validated_data.pop("sub_tasks")
        else:
            sub_tasks = {"create_sub_tasks": [], "update_sub_tasks": []}

        labels: list[models.Label] = validated_data.pop("labels")
        task = task_create_nested(
            who=request.user,
            section=section,
            title=validated_data["title"],
            description=validated_data.get("description"),
            assignee=validated_data.get("assignee"),
            due_date=validated_data.get("due_date"),
            labels=labels,
            sub_tasks=sub_tasks,
        )
        output_serializer = TaskDetailSerializer(instance=task)
        return Response(
            data=output_serializer.data, status=status.HTTP_201_CREATED
        )


# Read + Update + Delete
class TaskRetrieveUpdateDelete(APIView):
    """Retrieve a task."""

    @extend_schema(
        responses={200: TaskDetailSerializer},
    )
    def get(self, request: Request, task_uuid: UUID) -> Response:
        """Handle GET."""
        instance = get_object(request, task_uuid)
        serializer = TaskDetailSerializer(instance=instance)
        return Response(data=serializer.data)

    @extend_schema(
        request=TaskUpdateSerializer,
        responses={200: TaskDetailSerializer, 400: DeriveSchema},
    )
    def put(self, request: Request, task_uuid: UUID) -> Response:
        """
        Override update behavior. Return using different serializer.

        The idea is that we accept abbreviated nested fields, but return
        the data whole. (ws board section, sub tasks, labels, etc.)
        """
        # Copied from
        # https://github.com/encode/django-rest-framework/blob/d32346bae55f3e4718a185fb60e9f7a28e389c85/rest_framework/mixins.py#L65
        # We probably don't have to get the full object here!
        instance = get_object(request, task_uuid)
        serializer = TaskUpdateSerializer(
            instance,
            data=request.data,
            # Mild code duplication from
            # https://github.com/encode/django-rest-framework/blob/d32346bae55f3e4718a185fb60e9f7a28e389c85/rest_framework/generics.py#L113
            # :)
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        labels: list[models.Label] = validated_data.pop("labels")

        sub_tasks: ValidatedData
        if "sub_tasks" in validated_data:
            sub_tasks = validated_data.pop("sub_tasks")
        else:
            sub_tasks = {"create_sub_tasks": [], "update_sub_tasks": []}

        task_update_nested(
            who=request.user,
            task=instance,
            title=validated_data["title"],
            description=validated_data.get("description"),
            assignee=validated_data.get("assignee"),
            due_date=validated_data.get("due_date"),
            labels=labels,
            sub_tasks=sub_tasks,
        )

        instance = get_object(request, task_uuid)
        response_serializer = TaskDetailSerializer(instance=instance)
        return Response(
            status=status.HTTP_200_OK, data=response_serializer.data
        )

    @extend_schema(
        responses={204: None},
    )
    def delete(self, request: Request, task_uuid: UUID) -> Response:
        """Delete task."""
        instance = get_object(request, task_uuid)
        task_delete(task=instance, who=self.request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)


# RPC
class TaskMoveToSection(APIView):
    """Move a task to the beginning of a section."""

    class TaskMoveToSectionSerializer(serializers.Serializer):
        """Accept the target section uuid."""

        section_uuid = serializers.UUIDField()

    @extend_schema(
        request=TaskMoveToSectionSerializer,
        responses={200: TaskDetailSerializer, 400: DeriveSchema},
    )
    def post(self, request: Request, task_uuid: UUID) -> Response:
        """Process the request."""
        user = request.user
        serializer = self.TaskMoveToSectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        task = task_find_by_task_uuid(who=user, task_uuid=task_uuid)
        if task is None:
            raise NotFound(_("Task for this UUID not found"))
        section = section_find_for_user_and_uuid(
            section_uuid=data["section_uuid"],
            user=user,
        )
        if section is None:
            raise serializers.ValidationError(
                {"section_uuid": _("No section was found for the given uuid")}
            )
        task_move_after(task=task, who=user, after=section)
        task = task_find_by_task_uuid(
            who=user, task_uuid=task_uuid, qs=TaskDetailQuerySet
        )
        output_serializer = TaskDetailSerializer(instance=task)
        return Response(output_serializer.data, status=status.HTTP_200_OK)


# TODO inaccuracy: Might want to be able to move in front of a given task as
# well
class TaskMoveAfterTask(APIView):
    """Move a task right behind another task."""

    class TaskMoveAfterTaskSerializer(serializers.Serializer):
        """Accept a task uuid after which this task should be moved."""

        task_uuid = serializers.UUIDField()

    @extend_schema(
        request=TaskMoveAfterTaskSerializer,
        responses={200: TaskDetailSerializer, 400: DeriveSchema},
    )
    def post(self, request: Request, task_uuid: UUID) -> Response:
        """Process the request."""
        user = request.user
        serializer = self.TaskMoveAfterTaskSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        task = task_find_by_task_uuid(who=user, task_uuid=task_uuid)
        if task is None:
            raise NotFound(_("Task for this UUID not found"))
        after = task_find_by_task_uuid(task_uuid=data["task_uuid"], who=user)
        if after is None:
            raise serializers.ValidationError(
                {"after_task_uuid": _("No task was found for the given uuid")}
            )
        task_move_after(task=task, who=user, after=after)
        task = task_find_by_task_uuid(
            who=user, task_uuid=task_uuid, qs=TaskDetailQuerySet
        )
        output_serializer = TaskDetailSerializer(instance=task)
        return Response(output_serializer.data, status=status.HTTP_200_OK)
