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
"""Views for team member."""
from uuid import UUID

from django.utils.translation import gettext_lazy as _

from drf_spectacular.utils import extend_schema
from rest_framework import (
    serializers,
    views,
)
from rest_framework.exceptions import NotFound
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_204_NO_CONTENT

from projectify.lib.error_schema import DeriveSchema
from projectify.workspace.selectors.team_member import (
    team_member_find_by_team_member_uuid,
)
from projectify.workspace.serializers.base import (
    TeamMemberBaseSerializer,
)
from projectify.workspace.services.team_member import (
    team_member_delete,
    team_member_update,
)

from ..models.team_member import TeamMember


# Create
# Read + Update + Delete
class TeamMemberReadUpdateDelete(views.APIView):
    """Delete a team member."""

    @extend_schema(
        responses={200: TeamMemberBaseSerializer},
    )
    def get(self, request: Request, team_member_uuid: UUID) -> Response:
        """Handle GET."""
        team_member = team_member_find_by_team_member_uuid(
            who=request.user, team_member_uuid=team_member_uuid
        )
        if team_member is None:
            raise NotFound(_("Could not find team member for given UUID"))

        serializer = TeamMemberBaseSerializer(instance=team_member)

        return Response(status=HTTP_200_OK, data=serializer.data)

    class TeamMemberUpdateSerializer(serializers.ModelSerializer[TeamMember]):
        """Serializer for PUT updates."""

        class Meta:
            """Accept job_title, role."""

            fields = "job_title", "role"
            model = TeamMember

    @extend_schema(
        request=TeamMemberUpdateSerializer,
        responses={200: TeamMemberUpdateSerializer, 400: DeriveSchema},
    )
    def put(self, request: Request, team_member_uuid: UUID) -> Response:
        """Handle PUT."""
        team_member = team_member_find_by_team_member_uuid(
            who=request.user, team_member_uuid=team_member_uuid
        )
        if team_member is None:
            raise NotFound(_("Could not find team member for given UUID"))

        serializer = self.TeamMemberUpdateSerializer(
            data=request.data, instance=team_member
        )
        serializer.is_valid(raise_exception=True)
        team_member_update(
            team_member=team_member,
            who=request.user,
            role=serializer.validated_data["role"],
            job_title=serializer.validated_data.get("job_title"),
        )
        return Response(status=HTTP_200_OK, data=serializer.data)

    @extend_schema(
        responses={204: None},
    )
    def delete(self, request: Request, team_member_uuid: UUID) -> Response:
        """Handle DELETE."""
        team_member = team_member_find_by_team_member_uuid(
            who=request.user, team_member_uuid=team_member_uuid
        )
        if team_member is None:
            raise NotFound(_("Could not find team member for given UUID"))
        team_member_delete(who=self.request.user, team_member=team_member)
        return Response(status=HTTP_204_NO_CONTENT)
