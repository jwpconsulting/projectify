# SPDX-License-Identifier: AGPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 JWP Consulting GK

"""Hetzner settings."""

import os
import tomllib
import warnings
from pathlib import Path
from typing import Any

from projectify.settings.collect_static import CollectStatic

from .base import Base
from .types import StripeConfig


class Hetzner(Base):
    """
    Configuration for Hetzner deployment.

    See `docs/django-configuration.md` for details.
    """

    SITE_TITLE = "Projectify Production on Hetzner"
    # TODO remove default value
    ALLOWED_HOSTS = [os.getenv("ALLOWED_HOST", "www.projectifyapp.com")]
    FRONTEND_URL = f"https://{ALLOWED_HOSTS[0]}"

    STORAGES = CollectStatic.STORAGES

    SENDFILE_BACKEND = "django_sendfile.backends.xsendfile"

    @classmethod
    def setup(cls) -> None:
        """Load database config, after environment is correctly loaded."""
        cls.setup_runtime_directories()

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

        super().setup()

    @classmethod
    def setup_runtime_directories(cls) -> None:
        """Set up runtime directories for media and static files."""
        # Static files
        # We allow overriding this value in case the static files come prebuilt,
        # for example in a container, and an exact path is contained in
        # the STATIC_ROOT environment variable
        if "STATIC_ROOT" not in os.environ:
            warnings.warn(
                "Could not find STATIC_ROOT environment variable. "
                f"Falling back to Base.STATIC_ROOT={Base.STATIC_ROOT}"
            )
            cls.STATIC_ROOT = Base.STATIC_ROOT
        elif not Path(os.environ["STATIC_ROOT"]).exists():
            raise RuntimeError(
                f"The path STATIC_ROOT='{os.environ["STATIC_ROOT"]}' doesn't exist"
            )
        else:
            cls.STATIC_ROOT = Path(os.environ["STATIC_ROOT"])
        # TODO print friendly error when MEDIA_ROOT not found
        if "MEDIA_ROOT" not in os.environ:
            raise RuntimeError(
                "You need to set the MEDIA_ROOT environment variable"
            )
        elif not Path(os.environ["MEDIA_ROOT"]).exists():
            raise RuntimeError(
                f"The path MEDIA_ROOT='{os.environ["MEDIA_ROOT"]}' doesn't exist"
            )
        else:
            cls.MEDIA_ROOT = Path(os.environ["MEDIA_ROOT"])

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

        cls.STRIPE_CONFIG = StripeConfig(
            STRIPE_PUBLISHABLE_KEY=credentials["STRIPE_PUBLISHABLE_KEY"],
            STRIPE_SECRET_KEY=credentials["STRIPE_SECRET_KEY"],
            STRIPE_PRICE_OBJECT=credentials["STRIPE_PRICE_OBJECT"],
            STRIPE_ENDPOINT_SECRET=credentials["STRIPE_ENDPOINT_SECRET"],
        )

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
        """Load SMTP mail configuration."""
        if (
            "EMAIL_HOST" in credentials
            and "EMAIL_HOST_USER" in credentials
            and "EMAIL_HOST_PASSWORD" in credentials
        ):
            cls.EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
            # If you're using Lettermint, this is smtp.lettermint.co
            cls.EMAIL_HOST = credentials["EMAIL_HOST"]
            # Force implicit TLS, see also
            # https://lettermint.co/docs/guides/send-email-with-smtp#available-ports
            email_port = credentials.get("EMAIL_PORT", 465)
            if not isinstance(email_port, int):
                raise RuntimeError(
                    f"EMAIL_PORT must be an integer, received {email_port} ({type(email_port)})"
                )
            cls.EMAIL_PORT = email_port
            # Conditionally set explicit/implicit TLS settings
            cls.EMAIL_USE_TLS = email_port == 587
            cls.EMAIL_USE_SSL = email_port == 465
            # If you're using Lettermint, the user is lettermint
            cls.EMAIL_HOST_USER = credentials["EMAIL_HOST_USER"]
            # On Lettermint, this is your API token
            cls.EMAIL_HOST_PASSWORD = credentials["EMAIL_HOST_PASSWORD"]
        else:
            raise RuntimeError(
                f"You must specify the SMTP configuration in {credentials_file}"
            )
        if "DEFAULT_FROM_EMAIL" in credentials:
            cls.DEFAULT_FROM_EMAIL = credentials["DEFAULT_FROM_EMAIL"]

    @classmethod
    def post_setup(cls) -> None:
        """Warn if ADMINS is empty."""
        super().post_setup()
        if len(cls.ADMINS) == 0:
            warnings.warn(
                "No admin contacts set up. Set the ADMIN_EMAILS environment variable."
            )
