# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2021-2024 JWP Consulting GK
"""Production settings."""

import os
import warnings
from pathlib import Path

from .base import Base


class Production(Base):
    """Production configuration."""

    SITE_TITLE = os.getenv("SITE_TITLE", "Projectify Production")

    SECRET_KEY = os.environ["SECRET_KEY"]

    ALLOWED_HOSTS = os.environ["ALLOWED_HOSTS"].split(",")

    # TODO remove when Svelte frontend is gone
    FRONTEND_URL = os.environ["FRONTEND_URL"]

    ANYMAIL = {
        "MAILGUN_API_KEY": os.environ["MAILGUN_API_KEY"],
        "MAILGUN_SENDER_DOMAIN": os.environ["MAILGUN_DOMAIN"],
        "MAILGUN_API_URL": "https://api.eu.mailgun.net/v3",
    }
    EMAIL_BACKEND = "anymail.backends.mailgun.EmailBackend"

    # We want to permit multiple URLs here to allow migrating between hosts.
    # This way, we can have a standby available at another host already
    # configured with a new domain, but also letting old requests through
    # Doing so, we can switch over domain records to the new host and have it
    # immediately be ready to accept new requests
    # In ALLOWED_HOSTS we have already had this mechanism.
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

    CSRF_COOKIE_DOMAIN = os.getenv("CSRF_COOKIE_DOMAIN", None)

    # Stripe
    STRIPE_PUBLISHABLE_KEY = os.environ["STRIPE_PUBLISHABLE_KEY"]
    STRIPE_SECRET_KEY = os.environ["STRIPE_SECRET_KEY"]
    STRIPE_PRICE_OBJECT = os.environ["STRIPE_PRICE_OBJECT"]
    STRIPE_ENDPOINT_SECRET = os.environ["STRIPE_ENDPOINT_SECRET"]

    # Logging config
    LOGGING = Base.LOGGING
    LOGGING["handlers"]["mail_admins"] = {
        "level": "ERROR",
        "class": "django.utils.log.AdminEmailHandler",
    }

    @classmethod
    def setup(cls) -> None:
        """Set ADMINS from ADMIN_NAME and ADMIN_EMAIL."""
        super().setup()
        admin_name = os.getenv("ADMIN_NAME")
        if admin_name is None:
            warnings.warn("ADMIN_NAME environment variable not set")
        admin_email = os.getenv("ADMIN_EMAIL")
        if admin_email is None:
            warnings.warn("ADMIN_EMAIL environment variable not set")
        if admin_name and admin_email:
            cls.ADMINS = [[admin_name, admin_email]]

    @classmethod
    def post_setup(cls) -> None:
        """Warn if ADMINS is empty."""
        super().post_setup()
        if len(cls.ADMINS) == 0:
            warnings.warn(
                "No admin contacts set up. Set the ADMIN_EMAILS environment variable."
            )
