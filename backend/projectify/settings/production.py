# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Copyright (C) 2021-2024 JWP Consulting GK
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
"""Production settings."""

import logging
import os
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from projectify.lib.settings import populate_production_middleware

from .base import Base

logger = logging.getLogger(__name__)


def get_redis_tls_url() -> str:
    """Get the correct redis tls url, because Heroku."""
    # I am looking at you, Heroku :(((
    # Heroku unsets REDIS_TLS_URL when migrating to premium redis
    # TODO consider leaving Heroku (after 10 years!)
    if "REDIS_TLS_URL" in os.environ:
        return os.environ["REDIS_TLS_URL"]
    elif "REDIS_URL" in os.environ:
        return os.environ["REDIS_URL"]
    raise ValueError(
        "Neither REDIS_TLS_URL nor REDIS_URL could be found in the environment"
    )


def get_redis_channel_layer_hosts(redis_url: str) -> Mapping[str, Any]:
    """
    Return django channels redis config.

    If rediss:// URL is given IGNORE ssl cert requirements.

    Both options are equally bad IMO.
    """
    if redis_url.startswith("rediss://"):
        logger.warning(
            "Initializing channels redis layer with TLS url and instructing the redis client to ignore SSL certificate requirements!",
        )
        return {
            "hosts": [
                {
                    "address": redis_url,
                    "ssl_cert_reqs": None,
                }
            ],
        }
    else:
        logger.warning(
            "Initializing channels redis layer with non-TLS url and potentially"
            "transmitting queries in clear text!",
        )
        return {
            "hosts": [
                {
                    "address": redis_url,
                }
            ],
        }


class Production(Base):
    """Production configuration."""

    SITE_TITLE = os.getenv("SITE_TITLE", "Projectify Production")

    # Redis URL
    REDIS_TLS_URL = get_redis_tls_url()

    SECRET_KEY = os.environ["SECRET_KEY"]

    ALLOWED_HOSTS = os.environ["ALLOWED_HOSTS"].split(",")

    FRONTEND_URL = os.environ["FRONTEND_URL"]

    ANYMAIL = {
        "MAILGUN_API_KEY": os.environ["MAILGUN_API_KEY"],
        "MAILGUN_SENDER_DOMAIN": os.environ["MAILGUN_DOMAIN"],
    }
    EMAIL_BACKEND = "anymail.backends.mailgun.EmailBackend"

    # Celery
    CELERY_BROKER_URL = REDIS_TLS_URL

    # We want to permit multiple URLs here to allow migrating between hosts.
    # This way, we can have a standby available at another host already
    # configured with a new domain, but also letting old requests through
    # Doing so, we can switch over domain records to the new host and have it
    # immediately be ready to accept new requests
    # In ALLOWED_HOSTS we have already had this mechanism.
    CORS_ALLOWED_ORIGINS = os.getenv("SECURITY_ORIGINS", FRONTEND_URL).split(
        ","
    )
    CSRF_TRUSTED_ORIGINS = os.getenv("SECURITY_ORIGINS", FRONTEND_URL).split(
        ","
    )

    # Static files
    # We allow overriding this value in case the static files come prebuilt,
    # for example in a Docker container, and an exact path is contained in
    # the STATIC_ROOT environment variable
    STATIC_ROOT = (
        Path(os.environ["STATIC_ROOT"])
        if "STATIC_ROOT" in os.environ
        else Base.STATIC_ROOT
    )

    # Cloudinary
    STORAGES = {
        **Base.STORAGES,
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
        },
        "default": {
            "BACKEND": Base.MEDIA_CLOUDINARY_STORAGE,
        },
    }

    # Disable CSRF protection
    # TODO override this in a cleaner way
    # XXX actually, I don't know why we have it in the first place,
    # and at this point I am afraid to ask.
    MIDDLEWARE = list(populate_production_middleware(Base.MIDDLEWARE))

    CSRF_COOKIE_DOMAIN = os.getenv("CSRF_COOKIE_DOMAIN", ".projectifyapp.com")

    # Stripe
    STRIPE_PUBLISHABLE_KEY = os.environ["STRIPE_PUBLISHABLE_KEY"]
    STRIPE_SECRET_KEY = os.environ["STRIPE_SECRET_KEY"]
    STRIPE_PRICE_OBJECT = os.environ["STRIPE_PRICE_OBJECT"]
    STRIPE_ENDPOINT_SECRET = os.environ["STRIPE_ENDPOINT_SECRET"]

    # REDIS
    # https://devcenter.heroku.com/articles/connecting-heroku-redis#connecting-in-python
    # Obviously, this isn't great
    # https://github.com/django/channels_redis/issues/235
    # https://github.com/django/channels_redis/pull/337

    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels_redis.core.RedisChannelLayer",
            "CONFIG": {
                **get_redis_channel_layer_hosts(REDIS_TLS_URL),
                "symmetric_encryption_keys": [SECRET_KEY],
            },
        },
    }
