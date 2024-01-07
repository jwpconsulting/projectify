# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Copyright (C) 2021, 2022, 2023 JWP Consulting GK
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
import os
from collections.abc import (
    Iterable,
    Sequence,
)

from .. import (
    redis_helper,
)
from .base import (
    Base,
)


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


def populate_production_middleware(middleware: Sequence[str]) -> Iterable[str]:
    """Remove CORS middleware. No idea why we should do that."""
    csrf_middleware = "django.middleware.csrf.CsrfViewMiddleware"
    gzip_middleware = "django.middleware.gzip.GZipMiddleware"
    disable_csrf = "DISABLE_CSRF_PROTECTION" in os.environ
    for m in middleware:
        if m == csrf_middleware and disable_csrf:
            yield "projectify.middleware.DisableCSRFMiddleware"
            continue
        elif m == gzip_middleware:
            # Yield white noise *after* gzip
            yield m
            yield "whitenoise.middleware.WhiteNoiseMiddleware"
        else:
            yield m


class Production(Base):
    """Production configuration."""

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

    CORS_ALLOWED_ORIGINS = (
        "https://www.projectifyapp.com",
        "https://staging.projectifyapp.com",
        "http://localhost:3000",
    )
    CORS_ALLOWED_ORIGIN_REGEXES = (
        r"^https://deploy-preview-\d+--projectifyapp.netlify.app$",
        r"^https://.+--projectifyapp-staging.netlify.app$",
    )

    CSRF_TRUSTED_ORIGINS = (
        "https://*.netlify.app",
        "https://www.projectifyapp.com",
        "https://staging.projectifyapp.com",
        "http://localhost:3000",
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

    CSRF_COOKIE_DOMAIN = ".projectifyapp.com"

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
    redis_url = redis_helper.decode_redis_url(
        os.environ["REDIS_TLS_URL"],
    )

    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels_redis.core.RedisChannelLayer",
            "CONFIG": {
                "hosts": [
                    redis_helper.make_channels_redis_host(redis_url),
                ],
                "symmetric_encryption_keys": [SECRET_KEY],
            },
        },
    }
