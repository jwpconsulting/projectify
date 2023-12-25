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
