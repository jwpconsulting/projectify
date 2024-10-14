# SPDX-FileCopyrightText: 2024 JWP Consulting GK
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from collections.abc import Sequence
from typing import Type, Union

from django.views import (
    View,
)

from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.response import Response

def exception_handler(
    exc: Exception, context: object
) -> Union[Response, None]: ...

class APIView(View):
    request: Request
    permission_classes: Sequence[Type[BasePermission]]
