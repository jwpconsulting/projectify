# SPDX-License-Identifier: AGPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 JWP Consulting GK

"""Hetzner settings."""

import os
import tomllib
import warnings
from pathlib import Path
from typing import Any

from .base import Base


class Hetzner(Base):
    """
    Configuration for Hetzner deployment.

    Requires you to create a TOML file with the following keys:
    ADMIN_EMAIL=
    ADMIN_NAME=

    SECRET_KEY=

    ALLAUTH_GITHUB_CLIENT_ID=
    ALLAUTH_GITHUB_SECRET=
    ALLAUTH_GOOGLE_CLIENT_ID=
    ALLAUTH_GOOGLE_SECRET=

    MAILGUN_API_KEY=
    MAILGUN_DOMAIN=

    STRIPE_ENDPOINT_SECRET=
    STRIPE_PRICE_OBJECT=
    STRIPE_PUBLISHABLE_KEY=
    STRIPE_SECRET_KEY=
    """

    SITE_TITLE = "Projectify Production on Hetzner"
    ALLOWED_HOSTS = ["www.projectifyapp.com"]
    FRONTEND_URL = f"https://{ALLOWED_HOSTS[0]}"

    # Use file system to store media files
    STORAGES = {
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
        },
        # Caddy serves static files
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        },
    }
    # Caddy serves these media files:
    MEDIA_ROOT = Path(os.environ["MEDIA_ROOT"])
    # Static files
    # We allow overriding this value in case the static files come prebuilt,
    # for example in a container, and an exact path is contained in
    # the STATIC_ROOT environment variable
    STATIC_ROOT = (
        Path(os.environ["STATIC_ROOT"])
        if "STATIC_ROOT" in os.environ
        else Base.STATIC_ROOT
    )

    # Logging config
    LOGGING = Base.LOGGING
    LOGGING["handlers"]["mail_admins"] = {
        "level": "ERROR",
        "class": "django.utils.log.AdminEmailHandler",
    }

    # Emails
    EMAIL_BACKEND = "anymail.backends.mailgun.EmailBackend"

    @classmethod
    def setup(cls) -> None:
        """Load database config, after environment is correctly loaded."""
        super().setup()
        if "CREDENTIALS_FILE" not in os.environ:
            raise RuntimeError(
                "Expected environment variable CREDENTIALS_FILE to be set."
                "The Hetzner settings need this environment variable to "
                "correctly read all runtime settings."
            )
        credentials_file = Path(os.environ["CREDENTIALS_FILE"])
        try:
            with credentials_file.open("rb") as fp:
                credentials = tomllib.load(fp)
        except tomllib.TOMLDecodeError as e:
            raise RuntimeError(
                f"Could not parse credentials TOML file at {credentials_file}"
            ) from e
        except FileNotFoundError as e:
            raise RuntimeError(
                f"Could not find the credentials TOML file at {credentials_file}"
            ) from e

        if "SECRET_KEY" not in credentials:
            raise RuntimeError(
                f"You must specify SECRET_KEY in {credentials_file}"
            )
        cls.SECRET_KEY = credentials["SECRET_KEY"]

        cls.setup_allauth(credentials_file, credentials)
        cls.setup_billing(credentials_file, credentials)
        cls.setup_email(credentials_file, credentials)

        admin_name = credentials.get("ADMIN_NAME")
        if admin_name is None:
            warnings.warn("ADMIN_NAME environment variable not set")
        admin_email = credentials.get("ADMIN_EMAIL")
        if admin_email is None:
            warnings.warn("ADMIN_EMAIL environment variable not set")
        if admin_name and admin_email:
            cls.ADMINS = [[admin_name, admin_email]]

    @classmethod
    def setup_billing(
        cls, credentials_file: Path, credentials: dict[str, Any]
    ) -> None:
        """Load stripe configuration."""
        if "STRIPE_PUBLISHABLE_KEY" not in credentials:
            raise RuntimeError(
                f"You must specify the STRIPE_PUBLISHABLE_KEY in {credentials_file}"
            )
        if "STRIPE_SECRET_KEY" not in credentials:
            raise RuntimeError(
                f"You must specify the STRIPE_SECRET_KEY in {credentials_file}"
            )
        if "STRIPE_PRICE_OBJECT" not in credentials:
            raise RuntimeError(
                f"You must specify the STRIPE_PRICE_OBJECT in {credentials_file}"
            )
        if "STRIPE_ENDPOINT_SECRET" not in credentials:
            raise RuntimeError(
                f"You must specify the STRIPE_ENDPOINT_SECRET in {credentials_file}"
            )

        cls.STRIPE_PUBLISHABLE_KEY = credentials["STRIPE_PUBLISHABLE_KEY"]
        cls.STRIPE_SECRET_KEY = credentials["STRIPE_SECRET_KEY"]
        cls.STRIPE_PRICE_OBJECT = credentials["STRIPE_PRICE_OBJECT"]
        cls.STRIPE_ENDPOINT_SECRET = credentials["STRIPE_ENDPOINT_SECRET"]

    @classmethod
    def setup_allauth(
        cls, credentials_file: Path, credentials: dict[str, Any]
    ) -> None:
        """Load allauth configuration."""
        if (
            "ALLAUTH_GITHUB_CLIENT_ID" not in credentials
            or "ALLAUTH_GITHUB_SECRET" not in credentials
        ):
            raise RuntimeError(
                f"You must specify the GitHub OAuth credentials ALLAUTH_GITHUB_CLIENT_ID and ALLAUTH_GITHUB_SECRET in {credentials_file}"
            )

        cls.SOCIALACCOUNT_PROVIDERS["github"]["APPS"].append(
            {
                "client_id": credentials["ALLAUTH_GITHUB_CLIENT_ID"],
                "secret": credentials["ALLAUTH_GITHUB_SECRET"],
            }
        )

        if (
            "ALLAUTH_GOOGLE_CLIENT_ID" not in credentials
            or "ALLAUTH_GOOGLE_SECRET" not in credentials
        ):
            raise RuntimeError(
                f"You must specify the Google OAuth credentials ALLAUTH_GOOGLE_CLIENT_ID and ALLAUTH_GOOGLE_SECRET in {credentials_file}"
            )
        cls.SOCIALACCOUNT_PROVIDERS["google"]["APPS"].append(
            {
                "client_id": credentials["ALLAUTH_GOOGLE_CLIENT_ID"],
                "secret": credentials["ALLAUTH_GOOGLE_SECRET"],
            }
        )

    @classmethod
    def setup_email(
        cls, credentials_file: Path, credentials: dict[str, Any]
    ) -> None:
        """Load mailgun configuration."""
        if (
            "MAILGUN_API_KEY" not in credentials
            or "MAILGUN_DOMAIN" not in credentials
        ):
            raise RuntimeError(
                f"You must specify MAILGUN_API_KEY and MAILGUN_DOMAIN in {credentials_file}"
            )
        cls.ANYMAIL = {
            "MAILGUN_API_KEY": credentials["MAILGUN_API_KEY"],
            "MAILGUN_SENDER_DOMAIN": credentials["MAILGUN_DOMAIN"],
            "MAILGUN_API_URL": "https://api.eu.mailgun.net/v3",
        }

    @classmethod
    def post_setup(cls) -> None:
        """Warn if ADMINS is empty."""
        super().post_setup()
        if len(cls.ADMINS) == 0:
            warnings.warn(
                "No admin contacts set up. Set the ADMIN_EMAILS environment variable."
            )
