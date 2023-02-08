"""Redis connnection classes."""
from redis.asyncio import (
    connection,
)


class RedisConnection(connection.Connection):
    """SSL connection wrapper that allwows for custom ssl context."""

    def __init__(self, ssl_context, **kwargs):
        """Initialize SSL connection."""
        super().__init__(**kwargs)
        self.ssl_context = ssl_context
