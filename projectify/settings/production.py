"""Production settings."""
import os

from .. import (
    redis_helper,
)
from .base import (
    Base,
)


class Production(Base):
    """Production configuration."""

    # TODO write helper method for this if else
    # Redis URL
    # Heroku unsets REDIS_TLS_URL when migrating to premium redis
    if "REDIS_TLS_URL" not in os.environ:
        REDIS_TLS_URL = os.environ["REDIS_URL"]
    else:
        REDIS_TLS_URL = os.environ["REDIS_TLS_URL"]

    SECRET_KEY = os.environ["SECRET_KEY"]

    ALLOWED_HOSTS = os.environ["ALLOWED_HOSTS"].split(",")

    # TODO override this in a cleaner way
    STORAGES = Base.STORAGES
    STORAGES["staticfiles"][
        "BACKEND"
    ] = "whitenoise.storage.CompressedManifestStaticFilesStorage"

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

    # GraphQL
    # TODO ideally we would never have to set it to False here, only once
    # in the base settings
    GRAPHIQL_ENABLE = False

    # Cloudinary
    # TODO override this in a cleaner way
    STORAGES["default"]["BACKEND"] = Base.MEDIA_CLOUDINARY_STORAGE

    # Disable CSRF protection
    # TODO override this in a cleaner way
    # XXX actually, I don't know why we have it in the first place,
    # and at this point I am afraid to ask.
    csrf_middleware = "django.middleware.csrf.CsrfViewMiddleware"
    if "DISABLE_CSRF_PROTECTION" in os.environ:
        MIDDLEWARE = Base.MIDDLEWARE
        csrf_middleware_index = MIDDLEWARE.index(csrf_middleware)
        MIDDLEWARE[
            csrf_middleware_index
        ] = "projectify.middleware.DisableCSRFMiddleware"

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
