"""Contain some common types used among all models and querysets."""
from collections.abc import (
    Iterable,
    Sequence,
)
from typing import (
    Callable,
)


Pks = list[str]

GetOrder = Callable[[], Iterable[int]]
SetOrder = Callable[[Sequence[int]], None]
