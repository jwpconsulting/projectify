# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Copyright (C) 2024 JWP Consulting GK
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
"""User authentication views."""
from rest_framework import (
    serializers,
    views,
)
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT

from projectify.user.services.auth import (
    user_confirm_email,
    user_confirm_password_reset,
    user_log_in,
    user_log_out,
    user_request_password_reset,
    user_sign_up,
)


class LogOut(views.APIView):
    """Log a user out."""

    def post(self, request: Request) -> Response:
        """Handle POST."""
        user_log_out(request=request)
        return Response(status=HTTP_204_NO_CONTENT)


# The following views have no authentication required
class SignUp(views.APIView):
    """Sign up a user."""

    permission_classes = (AllowAny,)

    class InputSerializer(serializers.Serializer):
        """Take in email and password."""

        email = serializers.EmailField()
        password = serializers.CharField()
        tos_agreed = serializers.BooleanField()
        privacy_policy_agreed = serializers.BooleanField()

    def post(self, request: Request) -> Response:
        """Handle POST."""
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        user_sign_up(
            email=data["email"],
            password=data["password"],
            tos_agreed=data["tos_agreed"],
            privacy_policy_agreed=data["privacy_policy_agreed"],
        )
        return Response(status=HTTP_204_NO_CONTENT)


class ConfirmEmail(views.APIView):
    """Log a user in."""

    permission_classes = (AllowAny,)

    class InputSerializer(serializers.Serializer):
        """Take email and password."""

        email = serializers.EmailField()
        token = serializers.CharField()

    def post(self, request: Request) -> Response:
        """Handle POST."""
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        user_confirm_email(
            email=data["email"],
            token=data["token"],
        )
        return Response(status=HTTP_204_NO_CONTENT)


class LogIn(views.APIView):
    """Log a user in."""

    permission_classes = (AllowAny,)

    class InputSerializer(serializers.Serializer):
        """Take email and password."""

        email = serializers.EmailField()
        password = serializers.CharField()

    def post(self, request: Request) -> Response:
        """Handle POST."""
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        user_log_in(
            email=data["email"],
            password=data["password"],
            request=request,
        )
        return Response(status=HTTP_204_NO_CONTENT)


# Reset password
class PasswordResetRequest(views.APIView):
    """Request password to be reset."""

    permission_classes = (AllowAny,)

    class InputSerializer(serializers.Serializer):
        """Take an email address."""

        email = serializers.EmailField()

    def post(self, request: Request) -> Response:
        """Handle POST."""
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        user_request_password_reset(email=data["email"])
        return Response(status=HTTP_204_NO_CONTENT)


class PasswordResetConfirm(views.APIView):
    """Reset a user's password."""

    permission_classes = (AllowAny,)

    class InputSerializer(serializers.Serializer):
        """Take email, token and a new password."""

        email = serializers.EmailField()
        token = serializers.CharField()
        new_password = serializers.CharField()

    def post(self, request: Request) -> Response:
        """Handle POST."""
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        user_confirm_password_reset(
            email=data["email"],
            token=data["token"],
            new_password=data["new_password"],
        )
        return Response(status=HTTP_204_NO_CONTENT)
