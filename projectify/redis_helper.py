"""Redis connnection classes."""
from dataclasses import (
    dataclass,
)
from typing import (
    Any,
    Mapping,
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

    host: str
    port: int
    username: str
    password: str


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
