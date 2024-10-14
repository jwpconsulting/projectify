# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023 JWP Consulting GK
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
