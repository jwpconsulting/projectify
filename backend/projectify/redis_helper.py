# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Copyright (C) 2023 JWP Consulting GK
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
"""Redis connnection classes."""
from dataclasses import (
    dataclass,
)
from typing import (
    Any,
    Mapping,
    Optional,
)
from urllib.parse import (
    urlparse,
)

from redis.asyncio import (
    connection,
)


@dataclass
class RedisUrlParts:
    """Contains the relevant parts of a Redis TLS URL."""

    host: Optional[str]
    port: Optional[int]
    username: Optional[str]
    password: Optional[str]


def decode_redis_url(redis_url: str) -> RedisUrlParts:
    """Return the releveant parts of a Redis TLS URL."""
    parsed = urlparse(redis_url)
    return RedisUrlParts(
        host=parsed.hostname,
        port=parsed.port,
        username=parsed.username,
        password=parsed.password,
    )


def make_channels_redis_host(url_parts: RedisUrlParts) -> Mapping[str, Any]:
    """Make a channels redis configuration."""
    return {
        "host": url_parts.host,
        "port": url_parts.port,
        "username": url_parts.username,
        "password": url_parts.password,
        "connection_class": connection.SSLConnection,
        "ssl_cert_reqs": None,
    }
