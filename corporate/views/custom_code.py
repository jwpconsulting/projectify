"""Custom code views."""
from uuid import UUID

from django.utils.translation import gettext_lazy as _

from rest_framework import exceptions, serializers, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from corporate.services.custom_code import custom_code_redeem
from workspace.selectors.workspace import workspace_find_by_workspace_uuid


class CustomCodeRedeem(APIView):
    """Redeem a custom code for a workspace customer."""

    class InputSerializer(serializers.Serializer):
        """Serializer that takes in a CustomCode's code."""

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

        # Redeem custom code here
        custom_code_redeem(
            who=request.user, code=data["code"], workspace=workspace
        )
        return Response(status=status.HTTP_204_NO_CONTENT)
