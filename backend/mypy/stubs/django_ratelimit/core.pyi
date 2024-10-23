# Copyright (C) 2024 JWP Consulting GK
# SPDX-FileCopyrightText: 2024 JWP Consulting GK
#
# SPDX-License-Identifier: AGPL-3.0-or-later

"""Type stubs for django_ratelimit.core."""

from collections.abc import Callable
from typing import Literal, Optional, TypedDict, Union

from django.http import HttpRequest, HttpResponse

class Ratelimit(TypedDict):
    """Contain the fields returned by get_usage."""

    # Source
    # https://github.com/jsocol/django-ratelimit/blob/a2bfe2b5aceaa306e5358b7dea691f17259b0d67/django_ratelimit/core.py#L252
    count: int
    limit: int
    should_limit: bool
    time_left: int

Group = str
Rate = Union[str, tuple[int, int]]
RateFn = Callable[[Group, HttpRequest], Rate]
Method = Literal["DELETE", "PATCH", "POST", "PUT"]
ViewFunction = Callable[..., HttpResponse]

def get_usage(
    request: HttpRequest,
    group: Optional[str] = None,
    fn: Optional[ViewFunction] = None,
    key: Optional[str] = None,
    rate: Optional[Union[str, RateFn]] = None,
    method: Optional[Method] = None,
    increment: bool = False,
) -> Optional[Ratelimit]: ...
