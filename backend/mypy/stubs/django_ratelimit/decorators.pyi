# SPDX-FileCopyrightText: 2024 JWP Consulting GK
#
# SPDX-License-Identifier: AGPL-3.0-or-later

"""Django-ratelimit decorators."""

from collections.abc import Callable
from typing import Any, Literal, Optional, TypeVar

F = TypeVar("F", bound=Callable[..., Any])

Methods = Literal["DELETE", "PATCH", "POST", "PUT"]

def ratelimit(
    group: Optional[str] = None,
    key: Optional[str] = None,
    rate: Optional[str] = None,
    method: Optional[Methods] = None,
    block: Optional[bool] = True,
) -> Callable[[F], F]: ...
