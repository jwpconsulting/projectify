# SPDX-FileCopyrightText: 2024 JWP Consulting GK
#
# SPDX-License-Identifier: AGPL-3.0-or-later

"""DRF decorators."""

from collections.abc import Callable, Sequence
from typing import Any, Optional, Type, TypeVar

from rest_framework.permissions import BasePermission

F = TypeVar("F", bound=Callable[..., Any])

def api_view(
    http_method_names: Optional[Sequence[str]] = None,
) -> Callable[[F], F]: ...
def permission_classes(
    permission_classes: Sequence[Type[BasePermission]],
) -> Callable[[F], F]: ...

# TODO
# authentication_classes
# renderer_classes
# parser_classes
# throttle_classes
# schema
# action
