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
