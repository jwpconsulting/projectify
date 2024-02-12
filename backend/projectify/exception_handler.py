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
"""Override DRF's default exception handling."""
import logging
from typing import Optional, Union

from django.core.exceptions import (
    PermissionDenied,
)
from django.core.exceptions import (
    ValidationError as DjangoValidationError,
)
from django.http import Http404

from rest_framework.exceptions import (
    APIException,
)
from rest_framework.exceptions import (
    ValidationError as DrfValidationError,
)
from rest_framework.response import Response
from rest_framework.serializers import as_serializer_error
from rest_framework.views import exception_handler as drf_exception_handler

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
        case DjangoValidationError():
            result = DrfValidationError(as_serializer_error(exception))
        case PermissionDenied():
            logger.error("Permission denied: %s", exception)
            result = exception
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
