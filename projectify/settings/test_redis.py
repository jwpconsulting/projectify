"""Redis test settings."""
# TODO: This can be part of settings/test.py
import os

from .. import (
    redis_helper,
)
from .test import (
    Test,
)


class TestRedis(Test):
    """Settings used to test the connection to Redis."""

    # XXX when do we use this?
    # REDIS
    # https://devcenter.heroku.com/articles/connecting-heroku-redis#connecting-in-python
    # Obviously, this isn't great
    # https://github.com/django/channels_redis/issues/235
    # https://github.com/django/channels_redis/pull/337
    redis_url = redis_helper.decode_redis_url(
        os.environ["REDIS_TLS_URL"],
    )

    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels_redis.core.RedisChannelLayer",
            "CONFIG": {
                "hosts": (redis_helper.make_channels_redis_host(redis_url),),
            },
        },
    }
