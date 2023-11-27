from collections.abc import Sequence
from typing import Type

from django.views import (
    View,
)

from rest_framework.permissions import BasePermission

from . import (
    request,
)

class APIView(View):
    request: request.Request
    permission_classes: Sequence[Type[BasePermission]]
