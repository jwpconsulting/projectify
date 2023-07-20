"""Useful types for pytest fixtures."""
import contextlib
from collections.abc import (
    Callable,
    Mapping,
)
from typing import (
    Any,
)


Headers = Mapping[str, Any]
DjangoAssertNumQueries = Callable[
    [int], contextlib.AbstractContextManager[None]
]
