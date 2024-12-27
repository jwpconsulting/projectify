# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2022-2024 JWP Consulting GK
"""User app user model views."""

from typing import Union, cast

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import AnonymousUser
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _

from django_ratelimit.decorators import ratelimit
from rest_framework import parsers, serializers, views
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_204_NO_CONTENT

from projectify.lib.error_schema import DeriveSchema
from projectify.lib.schema import PolymorphicProxySerializer, extend_schema
from projectify.user.models import User
from projectify.user.serializers import (
    AnonymousUserSerializer,
    LoggedInUserSerializer,
)
from projectify.user.services.user import (
    user_change_password,
    user_confirm_email_address_update,
    user_request_email_address_update,
    user_update,
)


# Create
# Read
class UserRead(views.APIView):
    """Read user, regardless of logged in/out."""

    permission_classes = (AllowAny,)

    @extend_schema(
        responses={
            200: PolymorphicProxySerializer(
                "auth_info",
                [
                    LoggedInUserSerializer,
                    AnonymousUserSerializer,
                ],
                None,
            ),
        }
    )
    def get(self, request: Request) -> Response:
        """Handle GET."""
        user = cast(Union[User, AnonymousUser], request.user)
        serializer: serializers.Serializer
        if user.is_anonymous:
            serializer = AnonymousUserSerializer(
                instance={"kind": "unauthenticated"}
            )
        else:
            serializer = LoggedInUserSerializer(instance=user)
        return Response(data=serializer.data)


class UserUpdate(views.APIView):
    """Update user."""

    class UserUpdateSerializer(serializers.ModelSerializer[User]):
        """Take only preferred_name in."""

        class Meta:
            """Meta."""

            fields = ("preferred_name",)
            model = User

    @extend_schema(
        request=UserUpdateSerializer,
        responses={200: LoggedInUserSerializer, 400: DeriveSchema},
    )
    def put(self, request: Request) -> Response:
        """Update a user."""
        user = cast(Union[User, AnonymousUser], request.user)
        if not isinstance(user, User):
            raise PermissionDenied(
                _("Must be authenticated in order to update a user")
            )
        serializer = self.UserUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        user = user_update(
            who=user,
            user=user,
            preferred_name=data.get("preferred_name"),
        )
        output_serializer = LoggedInUserSerializer(instance=user)
        return Response(data=output_serializer.data, status=HTTP_200_OK)


# Delete


# RPC
# TODO merge this into user_update
class ProfilePictureUpload(views.APIView):
    """View that allows uploading a profile picture."""

    parser_classes = (parsers.MultiPartParser,)

    class ProfilePictureUploadSerializer(serializers.Serializer):
        """Deserialize picture upload."""

        file = serializers.ImageField(required=False)

    @extend_schema(
        request=ProfilePictureUploadSerializer,
        responses={204: None, 400: DeriveSchema},
    )
    def post(self, request: Request) -> Response:
        """Handle POST."""
        serializer = self.ProfilePictureUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        file_obj = serializer.validated_data.get("file", None)
        user = request.user
        if file_obj is None:
            user.profile_picture.delete()
        else:
            user.profile_picture = file_obj
        user.save()
        return Response(status=204)


class ChangePassword(views.APIView):
    """Allow changing password by specifying old and new password."""

    class ChangePasswordSerializer(serializers.Serializer):
        """Accept old and new password."""

        current_password = serializers.CharField()
        new_password = serializers.CharField()

    @extend_schema(
        request=ChangePasswordSerializer,
        responses={204: None, 400: DeriveSchema, 429: DeriveSchema},
    )
    @method_decorator(ratelimit(key="user", rate="5/h"))
    def post(self, request: Request) -> Response:
        """Handle POST."""
        user = request.user
        serializer = self.ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        user_change_password(
            user=user,
            current_password=data["current_password"],
            new_password=data["new_password"],
        )
        # Ensure we stay logged in
        # https://docs.djangoproject.com/en/5.0/topics/auth/default/#session-invalidation-on-password-change
        update_session_auth_hash(request, user)
        return Response(status=HTTP_204_NO_CONTENT)


class RequestEmailAddressUpdate(views.APIView):
    """Request an email address update."""

    class RequestEmailAddressUpdateSerializer(serializers.Serializer):
        """Accept new email."""

        password = serializers.CharField()
        new_email = serializers.EmailField()

    @extend_schema(
        request=RequestEmailAddressUpdateSerializer,
        responses={204: None, 400: DeriveSchema, 429: DeriveSchema},
    )
    @method_decorator(ratelimit(key="user", rate="5/h"))
    def post(self, request: Request) -> Response:
        """Handle POST."""
        user = request.user
        serializer = self.RequestEmailAddressUpdateSerializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        user_request_email_address_update(
            user=user,
            password=data["password"],
            new_email=data["new_email"],
        )
        return Response(status=HTTP_204_NO_CONTENT)


class ConfirmEmailAddressUpdate(views.APIView):
    """Confirm an email address update."""

    class ConfirmEmailAddressUpdateSerializer(serializers.Serializer):
        """Accept new email."""

        confirmation_token = serializers.CharField()

    @extend_schema(
        request=ConfirmEmailAddressUpdateSerializer,
        responses={
            204: None,
            400: DeriveSchema,
        },
    )
    def post(self, request: Request) -> Response:
        """Handle POST."""
        user = request.user
        serializer = self.ConfirmEmailAddressUpdateSerializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        user_confirm_email_address_update(
            user=user,
            confirmation_token=data["confirmation_token"],
        )
        return Response(status=HTTP_204_NO_CONTENT)
