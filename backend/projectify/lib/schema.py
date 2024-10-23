# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2024 JWP Consulting GK
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

        def __init__(self, *args: Any, **kwargs: Any) -> None:
            """Do nothing useful."""
            del args
            del kwargs

    class PolymorphicProxySerializer:  # type: ignore[no-redef]
        """Dummy PolymorphicProxySerializer."""

        def __init__(self, *args: Any, **kwargs: Any) -> None:
            """Do nothing useful."""
            del args
            del kwargs


__all__ = (
    "extend_schema",
    "OpenApiResponse",
    "PolymorphicProxySerializer",
    "_SchemaType",
)
