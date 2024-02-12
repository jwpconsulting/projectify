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
"""Coupon views."""
from uuid import UUID

from django.utils.translation import gettext_lazy as _

from rest_framework import exceptions, serializers, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from corporate.services.coupon import coupon_redeem
from workspace.selectors.workspace import workspace_find_by_workspace_uuid


class CouponRedeem(APIView):
    """Redeem a coupon for a workspace customer."""

    class InputSerializer(serializers.Serializer):
        """Serializer that takes in a Coupon's code."""

        code = serializers.CharField()

    def post(self, request: Request, workspace_uuid: UUID) -> Response:
        """Handle POST."""
        workspace = workspace_find_by_workspace_uuid(
            workspace_uuid=workspace_uuid,
            who=request.user,
        )
        if workspace is None:
            raise exceptions.NotFound(
                _("No workspace was found for this workspace uuid")
            )

        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        # Redeem coupon here
        coupon_redeem(who=request.user, code=data["code"], workspace=workspace)
        return Response(status=status.HTTP_204_NO_CONTENT)
