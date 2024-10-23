# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023 JWP Consulting GK
"""Useful types for pytest fixtures."""

import contextlib
from collections.abc import (
    Callable,
    Mapping,
    Sequence,
)
from typing import (
    Any,
)

from django.core.mail import EmailMessage

Headers = Mapping[str, Any]
DjangoAssertNumQueries = Callable[
    [int], contextlib.AbstractContextManager[None]
]
Mailbox = Sequence[EmailMessage]
