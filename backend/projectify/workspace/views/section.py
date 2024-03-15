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
"""Section views."""
from uuid import UUID

from django.utils.translation import gettext_lazy as _

from rest_framework import serializers, status
from rest_framework.exceptions import NotFound
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from projectify.workspace.models import (
    Section,
)
from projectify.workspace.selectors.project import (
    project_find_by_project_uuid,
)
from projectify.workspace.selectors.section import (
    SectionDetailQuerySet,
    section_find_for_user_and_uuid,
)
from projectify.workspace.serializers.section import (
    SectionDetailSerializer,
)
from projectify.workspace.services.section import (
    section_create,
    section_delete,
    section_move,
    section_update,
)


class SectionCreate(APIView):
    """Create a section."""

    class InputSerializer(serializers.ModelSerializer[Section]):
        """Parse section creation input."""

        project_uuid = serializers.UUIDField()

        class Meta:
            """Restrict fields to bare minimum needed for section creation."""

            model = Section
            fields = "title", "description", "project_uuid"

    def post(self, request: Request) -> Response:
        """Create a section."""
        user = request.user
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        project_uuid: UUID = data["project_uuid"]
        project = project_find_by_project_uuid(
            project_uuid=project_uuid,
            who=request.user,
            archived=False,
        )
        if project is None:
            raise serializers.ValidationError(
                {
                    "project_uuid": _(
                        "Could not find a project with this uuid"
                    )
                }
            )
        section = section_create(
            project=project,
            title=data["title"],
            description=data.get("description"),
            who=user,
        )
        output_serializer = SectionDetailSerializer(
            instance=section,
        )
        return Response(data=output_serializer.data, status=201)


# Read + Update + Delete
class SectionReadUpdateDelete(APIView):
    """Project retrieve view."""

    def get(self, request: Request, section_uuid: UUID) -> Response:
        """Handle GET."""
        section = section_find_for_user_and_uuid(
            user=request.user,
            section_uuid=section_uuid,
            qs=SectionDetailQuerySet,
        )
        if section is None:
            raise NotFound(_("Section not found for this UUID"))
        serializer = SectionDetailSerializer(instance=section)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    class InputSerializer(serializers.ModelSerializer[Section]):
        """Input serializer for PUT."""

        class Meta:
            """Accept title and description."""

            fields = "title", "description"
            model = Section

    def put(self, request: Request, section_uuid: UUID) -> Response:
        """Update section."""
        section = section_find_for_user_and_uuid(
            user=request.user,
            section_uuid=section_uuid,
            qs=SectionDetailQuerySet,
        )
        if section is None:
            raise NotFound(_("Section not found for this UUID"))

        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        section_update(
            who=request.user,
            section=section,
            title=serializer.validated_data["title"],
            description=serializer.validated_data.get("description"),
        )
        return Response(data=serializer.validated_data)

    def delete(self, request: Request, section_uuid: UUID) -> Response:
        """Handle DELETE."""
        section = section_find_for_user_and_uuid(
            user=request.user,
            section_uuid=section_uuid,
            qs=SectionDetailQuerySet,
        )
        if section is None:
            raise NotFound(_("Section not found for this UUID"))
        section_delete(
            who=self.request.user,
            section=section,
        )
        return Response(status=status.HTTP_204_NO_CONTENT)


# RPC
class SectionMove(APIView):
    """Insert a section at a given position."""

    class InputSerializer(serializers.Serializer):
        """Accept the desired position within project."""

        order = serializers.IntegerField()

    def post(self, request: Request, section_uuid: UUID) -> Response:
        """Process request."""
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        user = request.user
        section = section_find_for_user_and_uuid(
            user=request.user,
            section_uuid=section_uuid,
            qs=SectionDetailQuerySet,
        )
        if section is None:
            raise NotFound(_("Section not found for this UUID"))
        section_move(
            section=section,
            order=data["order"],
            who=user,
        )
        section.refresh_from_db()
        return Response(status=status.HTTP_200_OK)
