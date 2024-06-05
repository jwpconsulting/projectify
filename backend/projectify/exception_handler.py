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
"""
Override DRF's default exception handling.

Serialize validation errors into something we can handle with types in the
frontend.

Reject errors that we can't serialize with a logger warning and return None
for that error.

Is it OK to deal with errors like that? Validation errors are part of the
UI and if we can't render them correctly, then that's a bug.

Other errors in the 500 category we don't show to the user anyway, and the
purpose of a 400 error is to give the user the opportunity to correct the
error itself.
"""
import logging
from collections.abc import Mapping, Sequence
from typing import Literal, Optional, TypedDict, Union

from django.core.exceptions import (
    NON_FIELD_ERRORS,
    PermissionDenied,
)
from django.core.exceptions import (
    ValidationError as DjangoValidationError,
)
from django.http import Http404

from rest_framework import serializers, status
from rest_framework.exceptions import (
    APIException,
    ErrorDetail,
    Throttled,
)
from rest_framework.response import Response
from rest_framework.serializers import as_serializer_error
from rest_framework.views import exception_handler as drf_exception_handler

from projectify.lib.settings import get_settings

logger = logging.getLogger(__name__)

# From the DRF docs:
# The handled exceptions are:
# Subclasses of APIException raised inside REST framework.
# Django's Http404 exception.
# Django's PermissionDenied exception.
DRFError = APIException
DjangoError = Union[Http404, PermissionDenied]
# We create a union for the above,
DrfHandledException = Union[DRFError, DjangoError]
# and then we add Django's ValidationError to it as well.
# Theoretically it could be another error as well, so we add Exception to it as
# well and call it HandledException:
HandledException = Union[
    DRFError,
    DjangoError,
    DjangoValidationError,
    # Here be dragons
    Exception,
]

# The below is somewhat like this:
# interface error {
#   status: "error";
#   code: int;
#   details?: ErrorContent;
#   general?: ErrorContent;
# }
# type ErrorContent =
# | ["string", string]
# | ["list", ErrorContent]
# | ["dict", Record<str, ErrorContent>]

# This is designed with nested serializers in mind


# What we get from DRF:
SerializerErrorField = Union[
    tuple[ErrorDetail],
    list[ErrorDetail],
    list["SerializerErrorField"],
    dict[str, "SerializerErrorField"],
]
SerializerError = dict[str, SerializerErrorField]


# What we produce:
ErrorContent = Union[str, Sequence[Mapping[str, "ErrorContent"]]]
ErrorRootBadRequest = TypedDict(
    "ErrorRootBadRequest",
    {
        "status": Literal["error"],
        "code": Literal[400],
        "details": Mapping[str, ErrorContent],
        "general": Optional[str],
    },
)
ErrorRootTooManyRequests = TypedDict(
    "ErrorRootTooManyRequests",
    {
        "status": Literal["error"],
        "code": Literal[429],
    },
)
ErrorRoot = Union[ErrorRootBadRequest, ErrorRootTooManyRequests]


def serialize_error_dict(
    field: SerializerErrorField,
) -> Optional[Mapping[str, ErrorContent]]:
    """Serialize a dict containing validation error details."""
    match field:
        case dict() as d:
            return {
                k: v
                for k, v in (
                    (k, serialize_error_list(v)) for k, v in d.items()
                )
                if v
            }
        case _:
            logger.warning(
                "Don't know how to serialize single error list %s", field
            )
            return None


def serialize_error_list(
    field: SerializerErrorField,
) -> Optional[ErrorContent]:
    """Serialize a list containing validation error details."""
    match field:
        case (ErrorDetail() as s,):
            return str(s)
        case list() as l:
            # Clunky type casting
            result: list[Mapping[str, ErrorContent]] = []
            for i in l:
                if isinstance(i, ErrorDetail):
                    logger.warning("Dropping single ErrorDetail %s", i)
                    continue
                ser = serialize_error_dict(i)
                if ser is None:
                    logger.warning("Dropping item %s.", i)
                    continue
                result.append(ser)
            return result
        case _:
            logger.warning("Don't know how to serialize error list %s", field)
            return None


settings = get_settings()


def serialize_validation_error(
    error: Union[DjangoValidationError, serializers.ValidationError],
) -> ErrorRoot:
    """Serialize a validation error."""
    details = as_serializer_error(error)
    # In Django, (not DRF!) check constraints end up as "__all__", so we put
    # them somewhere more useful
    django_non_field_errors = details.pop(NON_FIELD_ERRORS, None)
    # drf_general is set in projectify/settings/base.py
    drf_non_field_errors = details.pop("drf_general", None)

    serialized = serialize_error_dict(details)

    general: list[SerializerErrorField] = []
    if django_non_field_errors is not None:
        general.append(django_non_field_errors)
    if drf_non_field_errors is not None:
        general.append(drf_non_field_errors)

    general_str: Optional[str]
    match general:
        case []:
            general_str = None
        case [[ErrorDetail() as e], *rest]:
            if rest:
                logger.warning("Could not serialize errors %s", rest)
            general_str = str(e)
        case _:
            logger.warning("Could not serialize errors %s", general)
            general_str = None
    return {
        "status": "error",
        "code": 400,
        "details": serialized or {},
        "general": general_str,
    }


class TooManyRequestsSerializer(serializers.Serializer):
    """Serialize 429 too many requests error."""

    status = serializers.ChoiceField(choices=["error"], default="error")
    code = serializers.ChoiceField(choices=[429], source="status_code")


# TODO find out what ctx is
def exception_handler(
    exception: HandledException, ctx: object
) -> Optional[Response]:
    """
    Handle exceptions for DRF.

    1. Accept django's ValidationError and DRF ValidationError
    2. Wrap them in a {"error": { ...errors }} dict (TODO)
    3. Give them as a Response
    """
    result: HandledException
    match exception:
        case DjangoValidationError() | serializers.ValidationError():
            data = serialize_validation_error(exception)
            return Response(status=status.HTTP_400_BAD_REQUEST, data=data)
        case PermissionDenied():
            logger.error("Permission denied: %s", exception)
            result = exception
        case Throttled():
            serializer = TooManyRequestsSerializer(exception)
            return Response(
                status=status.HTTP_429_TOO_MANY_REQUESTS, data=serializer.data
            )
        case APIException():
            logger.error("DRF API Exception: %s", exception)
            result = exception
        case Http404():
            logger.error("404: %s", exception)
            result = exception
        case Exception():
            logger.error("Unhandleable exception: %s", exception)
            result = exception

    return drf_exception_handler(result, ctx)
