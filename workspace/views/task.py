# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Copyright (C) 2023-2024 JWP Consulting GK
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""Task CRUD views."""
from uuid import UUID

from django.utils.translation import gettext_lazy as _

from rest_framework import (
    serializers,
    status,
)
from rest_framework.exceptions import NotFound
from rest_framework.request import (
    Request,
)
from rest_framework.response import (
    Response,
)
from rest_framework.views import APIView

from workspace.models.workspace_board_section import WorkspaceBoardSection
from workspace.selectors.task import TaskDetailQuerySet, task_find_by_task_uuid
from workspace.selectors.workspace_board_section import (
    workspace_board_section_find_for_user_and_uuid,
)
from workspace.serializers.base import TaskBaseSerializer
from workspace.serializers.task_detail import (
    TaskCreateUpdateSerializer,
    TaskDetailSerializer,
)
from workspace.services.sub_task import ValidatedData
from workspace.services.task import (
    task_create_nested,
    task_delete,
    task_move_after,
    task_update_nested,
)

from .. import (
    models,
)


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

    def post(self, request: Request) -> Response:
        """Handle POST."""
        serializer = TaskCreateUpdateSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        workspace_board_section: WorkspaceBoardSection = validated_data[
            "workspace_board_section"
        ]

        sub_tasks: ValidatedData
        if "sub_tasks" in validated_data:
            sub_tasks = validated_data.pop("sub_tasks")
        else:
            sub_tasks = {"create_sub_tasks": [], "update_sub_tasks": []}

        labels: list[models.Label] = validated_data.pop("labels")
        task = task_create_nested(
            who=request.user,
            workspace_board_section=workspace_board_section,
            title=validated_data["title"],
            description=validated_data.get("description"),
            assignee=validated_data.get("assignee"),
            due_date=validated_data.get("due_date"),
            labels=labels,
            sub_tasks=sub_tasks,
        )
        output_serializer = TaskBaseSerializer(instance=task)
        return Response(
            data=output_serializer.data, status=status.HTTP_201_CREATED
        )


# Read + Update + Delete
class TaskRetrieveUpdateDelete(APIView):
    """Retrieve a task."""

    def get(self, request: Request, task_uuid: UUID) -> Response:
        """Handle GET."""
        instance = get_object(request, task_uuid)
        serializer = TaskDetailSerializer(instance=instance)
        return Response(data=serializer.data)

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
        serializer = TaskCreateUpdateSerializer(
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
        return Response(response_serializer.data)

    def delete(self, request: Request, task_uuid: UUID) -> Response:
        """Delete task."""
        instance = get_object(request, task_uuid)
        task_delete(task=instance, who=self.request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)


# RPC
class TaskMoveToWorkspaceBoardSection(APIView):
    """Move a task to the beginning of a workspace board section."""

    class InputSerializer(serializers.Serializer):
        """Accept the target workspace board section uuid."""

        workspace_board_section_uuid = serializers.UUIDField()

    def post(self, request: Request, task_uuid: UUID) -> Response:
        """Process the request."""
        user = request.user
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        task = task_find_by_task_uuid(who=user, task_uuid=task_uuid)
        if task is None:
            raise NotFound(_("Task for this UUID not found"))
        workspace_board_section = (
            workspace_board_section_find_for_user_and_uuid(
                workspace_board_section_uuid=data[
                    "workspace_board_section_uuid"
                ],
                user=user,
            )
        )
        if workspace_board_section is None:
            raise serializers.ValidationError(
                {
                    "workspace_board_section_uuid": _(
                        "No workspace board section was found for the given uuid"
                    )
                }
            )
        task_move_after(task=task, who=user, after=workspace_board_section)
        task = task_find_by_task_uuid(
            who=user, task_uuid=task_uuid, qs=TaskDetailQuerySet
        )
        output_serializer = TaskDetailSerializer(instance=task)
        return Response(output_serializer.data, status=status.HTTP_200_OK)


# TODO inaccuracy: Might want to be able to move in front of a given task as
# well
class TaskMoveAfterTask(APIView):
    """Move a task right behind another task."""

    class InputSerializer(serializers.Serializer):
        """Accept a task uuid after which this task should be moved."""

        task_uuid = serializers.UUIDField()

    def post(self, request: Request, task_uuid: UUID) -> Response:
        """Process the request."""
        user = request.user
        serializer = self.InputSerializer(data=request.data)
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
