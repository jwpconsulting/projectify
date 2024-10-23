# SPDX-FileCopyrightText: 2024 JWP Consulting GK
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from collections.abc import (
    Awaitable,
)
from typing import (
    Callable,
    ParamSpec,
    TypeVar,
)

T = TypeVar("T")
R = TypeVar("R")
P = ParamSpec("P")

def database_sync_to_async(
    fn: Callable[P, R],
) -> Callable[P, Awaitable[R]]: ...
