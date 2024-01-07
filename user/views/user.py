# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Copyright (C) 2022, 2023 JWP Consulting GK
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
"""User app user model views."""
from typing import (
    Union,
    cast,
)

from django.contrib.auth.models import AnonymousUser
from django.utils.translation import gettext_lazy as _

from rest_framework import (
    parsers,
    serializers,
    views,
)
from rest_framework.exceptions import NotAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_204_NO_CONTENT

from user.models import User
from user.serializers import UserSerializer
from user.services.user import (
    user_confirm_email,
    user_confirm_password_reset,
    user_log_in,
    user_log_out,
    user_request_password_reset,
    user_sign_up,
    user_update,
)


# Create
# Read + Update
class UserReadUpdate(views.APIView):
    """Read or update user."""

    permission_classes = (AllowAny,)

    class UpdateInputSerializer(serializers.ModelSerializer[User]):
        """Take only full_name in."""

        class Meta:
            """Meta."""

            fields = ("full_name",)
            model = User

    def get(self, request: Request) -> Response:
        """Handle GET."""
        user = cast(Union[User, AnonymousUser], request.user)
        if user.is_anonymous:
            return Response(data={"unauthenticated": True})
        serializer = UserSerializer(instance=user)
        return Response(data=serializer.data)

    def put(self, request: Request) -> Response:
        """Update a user."""
        user = cast(Union[User, AnonymousUser], request.user)
        if not isinstance(user, User):
            raise NotAuthenticated(
                _("Must be authenticated in order to update a user")
            )
        serializer = self.UpdateInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        user = user_update(
            who=user,
            user=user,
            full_name=data.get("full_name"),
        )
        output_serializer = UserSerializer(instance=user)
        return Response(data=output_serializer.data, status=HTTP_200_OK)


# Delete


# RPC
# TODO merge this into user_update
class ProfilePictureUpload(views.APIView):
    """View that allows uploading a profile picture."""

    parser_classes = (parsers.MultiPartParser,)

    def post(self, request: Request) -> Response:
        """Handle POST."""
        file_obj = request.data.get("file", None)
        user = request.user
        if file_obj is None:
            user.profile_picture.delete()
        else:
            user.profile_picture = file_obj
        user.save()
        return Response(status=204)


# TODO these should be in user/views/auth.py
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
