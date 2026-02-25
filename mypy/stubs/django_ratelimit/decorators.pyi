# SPDX-FileCopyrightText: 2024 JWP Consulting GK
#
# SPDX-License-Identifier: AGPL-3.0-or-later

"""Django-ratelimit decorators."""

from collections.abc import Callable
from typing import Any, Optional, TypeVar

from django_ratelimit.core import Method

F = TypeVar("F", bound=Callable[..., Any])

def ratelimit(
    group: Optional[str] = None,
    key: Optional[str] = None,
    rate: Optional[str] = None,
    method: Optional[Method] = None,
    block: Optional[bool] = True,
) -> Callable[[F], F]: ...
