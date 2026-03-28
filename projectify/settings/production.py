# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2021-2024 JWP Consulting GK
"""Production settings."""

import os
import warnings
from pathlib import Path

from django.utils.csp import CSP  # type: ignore

from .base import Base


# TODO make this
# class Production(Base):
class ProductionBase(Base):
    """Production base configuration."""

    SITE_TITLE = os.getenv("SITE_TITLE", "Projectify Production")

    SECRET_KEY = os.environ["SECRET_KEY"]

    ALLOWED_HOSTS = os.environ["ALLOWED_HOSTS"].split(",")

    # TODO remove when Svelte frontend is gone
    FRONTEND_URL = os.environ["FRONTEND_URL"]

    # TODO remove FRONTEND_URL fallback
    CSRF_TRUSTED_ORIGINS = os.getenv("SECURITY_ORIGINS", FRONTEND_URL).split(
        ","
    )

    # Static files
    # We allow overriding this value in case the static files come prebuilt,
    # for example in a container, and an exact path is contained in
    # the STATIC_ROOT environment variable
    STATIC_ROOT = (
        Path(os.environ["STATIC_ROOT"])
        if "STATIC_ROOT" in os.environ
        else Base.STATIC_ROOT
    )

    STORAGES = {
        **Base.STORAGES,
        "default": {
            "BACKEND": Base.MEDIA_CLOUDINARY_STORAGE,
        },
    }

    CSRF_COOKIE_DOMAIN = os.getenv("CSRF_COOKIE_DOMAIN", None)

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


# TODO make this
# class Hosted(Production):
class Production(ProductionBase):
    """Settings for Projectify hosted on www.projectifyapp.com."""

    INSTALLED_APPS = (
        *ProductionBase.INSTALLED_APPS,
        "cloudinary",
        "cloudinary_storage",
    )
    ANYMAIL = {
        "MAILGUN_API_KEY": os.environ["MAILGUN_API_KEY"],
        "MAILGUN_SENDER_DOMAIN": os.environ["MAILGUN_DOMAIN"],
        "MAILGUN_API_URL": "https://api.eu.mailgun.net/v3",
    }
    EMAIL_BACKEND = "anymail.backends.mailgun.EmailBackend"

    # Stripe
    STRIPE_PUBLISHABLE_KEY = os.environ["STRIPE_PUBLISHABLE_KEY"]
    STRIPE_SECRET_KEY = os.environ["STRIPE_SECRET_KEY"]
    STRIPE_PRICE_OBJECT = os.environ["STRIPE_PRICE_OBJECT"]
    STRIPE_ENDPOINT_SECRET = os.environ["STRIPE_ENDPOINT_SECRET"]

    # Cloudinary
    MEDIA_CLOUDINARY_STORAGE = (
        "cloudinary_storage.storage.MediaCloudinaryStorage"
    )
    STORAGES = {
        # TODO make this
        # **Production.STORAGES,
        **ProductionBase.STORAGES,
        "default": {
            "BACKEND": MEDIA_CLOUDINARY_STORAGE,
        },
    }
    SECURE_CSP = {
        **ProductionBase.SECURE_CSP,
        "img-src": [CSP.SELF, "res.cloudinary.com"],
    }


# TODO remove this and just keep the above Hosted(Production)
# class Hosted(Production):
class Hosted(Production):
    """Settings for Projectify hosted on www.projectifyapp.com."""
