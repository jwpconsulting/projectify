# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Copyright (C) 2022-2024 JWP Consulting GK
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

from projectify.user.models import User
from projectify.user.serializers import UserSerializer
from projectify.user.services.user import (
    user_change_password,
    user_update,
)


# Create
# Read + Update
class UserReadUpdate(views.APIView):
    """Read or update user."""

    permission_classes = (AllowAny,)

    class UpdateInputSerializer(serializers.ModelSerializer[User]):
        """Take only preferred_name in."""

        class Meta:
            """Meta."""

            fields = ("preferred_name",)
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
            preferred_name=data.get("preferred_name"),
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


class ChangePassword(views.APIView):
    """Allow changing password by specifying old and new password."""

    class InputSerializer(serializers.Serializer):
        """Accept old and new password."""

        old_password = serializers.CharField()
        new_password = serializers.CharField()

    def post(self, request: Request) -> Response:
        """Handle POST."""
        user = request.user
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        user_change_password(
            user=user,
            old_password=data["old_password"],
            new_password=data["new_password"],
        )
        return Response(status=HTTP_204_NO_CONTENT)
