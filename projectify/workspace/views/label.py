# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Copyright (C) 2023 JWP Consulting GK
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
"""Label views."""
from uuid import UUID

from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_204_NO_CONTENT
from rest_framework.views import APIView

from projectify.workspace.models.label import Label
from projectify.workspace.models.workspace import Workspace
from projectify.workspace.serializers.base import LabelBaseSerializer
from projectify.workspace.services.label import (
    label_create,
    label_delete,
    label_update,
)


# Create
class LabelCreate(APIView):
    """View for creating labels."""

    class InputSerializer(serializers.ModelSerializer[Label]):
        """Serializer for label creation."""

        workspace_uuid = serializers.UUIDField()

        class Meta:
            """Meta."""

            fields = "name", "color", "workspace_uuid"
            model = Label

    def post(self, request: Request) -> Response:
        """Create the label."""
        user = request.user
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        workspace_uuid: UUID = data["workspace_uuid"]
        try:
            workspace = Workspace.objects.filter_for_user_and_uuid(
                uuid=workspace_uuid,
                user=user,
            ).get()
        except Workspace.DoesNotExist:
            raise serializers.ValidationError(
                {
                    "workspace_uuid": _(
                        "No workspace could be found for given workspace_uuid"
                    ),
                }
            )
        label = label_create(
            workspace=workspace,
            name=data["name"],
            color=data["color"],
            who=user,
        )
        output_serializer = LabelBaseSerializer(instance=label)
        return Response(output_serializer.data, status=201)


class LabelUpdateDelete(APIView):
    """View for updating labels."""

    class InputSerializer(serializers.ModelSerializer[Label]):
        """Serializer for Label update."""

        class Meta:
            """Meta."""

            fields = "name", "color"
            model = Label

    def get_label(self, request: Request, label_uuid: UUID) -> Label:
        """Get the requested label."""
        label_qs = Label.objects.filter_for_user_and_uuid(
            user=request.user, uuid=label_uuid
        )
        return get_object_or_404(label_qs)

    def put(self, request: Request, label_uuid: UUID) -> Response:
        """Handle PUT."""
        label = self.get_label(request, label_uuid)
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        label = label_update(
            who=request.user,
            label=label,
            name=data["name"],
            color=data["color"],
        )
        output_serializer = LabelBaseSerializer(instance=label)
        return Response(data=output_serializer.data, status=HTTP_200_OK)

    def delete(self, request: Request, label_uuid: UUID) -> Response:
        """Handle DELETE."""
        label = self.get_label(request, label_uuid)
        label_delete(label=label, who=request.user)
        return Response(status=HTTP_204_NO_CONTENT)
