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
Override spectacular's schema utils.

Allows us to run production code without needing for spectacular to be
present.
"""

from typing import Any, Callable, Dict, TypeVar

from rest_framework.fields import empty

F = TypeVar("F", bound=Callable[..., Any])


def extend_schema(
    request: Any = empty, responses: Any = empty
) -> Callable[[F], F]:
    """Lazily load extend_schema."""
    try:
        from drf_spectacular.utils import extend_schema as _extend_schema
    except ImportError:
        return lambda x: x
    return _extend_schema(request=request, responses=responses)


_SchemaType = Dict[str, Any]


try:
    from drf_spectacular.utils import (
        OpenApiResponse,
        PolymorphicProxySerializer,
    )
except ModuleNotFoundError:

    class OpenApiResponse:  # type: ignore[no-redef]
        """Dummy OpenApiResponse."""

        def init(self, *args: Any, **kwargs: Any) -> None:
            """Do nothing useful."""
            del args
            del kwargs

    class PolymorphicProxySerializer:  # type: ignore[no-redef]
        """Dummy PolymorphicProxySerializer."""

        def init(self, *args: Any, **kwargs: Any) -> None:
            """Do nothing useful."""
            del args
            del kwargs


__all__ = (
    "extend_schema",
    "OpenApiResponse",
    "PolymorphicProxySerializer",
    "_SchemaType",
)
