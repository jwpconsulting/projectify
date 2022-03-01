"""Production settings."""
import os
import ssl

# flake8: noqa: F401, F403
from .base import *


SECRET_KEY = os.environ["SECRET_KEY"]

ALLOWED_HOSTS = os.environ["ALLOWED_HOSTS"].split(",")

# Want forever-cacheable files and compression support? Just add this to your settings.py:
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

FRONTEND_URL = os.environ["FRONTEND_URL"]

ANYMAIL = {
    "MAILGUN_API_KEY": os.environ["MAILGUN_API_KEY"],
    "MAILGUN_SENDER_DOMAIN": os.environ["MAILGUN_DOMAIN"],
}
EMAIL_BACKEND = "anymail.backends.mailgun.EmailBackend"

# Celery
CELERY_BROKER_URL = os.environ["REDIS_TLS_URL"]

CORS_ALLOWED_ORIGINS = ("https://www.projectifyapp.com",)
CORS_ALLOWED_ORIGIN_REGEXES = (
    r"^https://deploy-preview-\d+--projectifyapp.netlify.app$",
)

CSRF_TRUSTED_ORIGINS = (
    "https://*.netlify.app",
    "https://www.projectifyapp.com",
)

# GraphQL
GRAPHIQL_ENABLE = False
GRAPHQL_WS_SEQUENTIAL = False

# Channels
# https://github.com/django/channels_redis/issues/235#issuecomment-795520644
ssl_context = ssl.SSLContext()
ssl_context.check_hostname = False

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = True

SECURE_HSTS_SECONDS = 3600

heroku_redis_ssl_host = {
    "address": os.environ["REDIS_TLS_URL"],
    "ssl": ssl_context,
}
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": (heroku_redis_ssl_host,),
            "symmetric_encryption_keys": [SECRET_KEY],
        },
    },
}

# Cloudinary
DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"
