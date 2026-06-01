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

    STORAGES = CollectStatic.STORAGES

    SENDFILE_BACKEND = "django_sendfile.backends.xsendfile"

    @classmethod
    def setup(cls) -> None:
        """Load database config, after environment is correctly loaded."""
        cls.setup_runtime_directories()
        cls.setup_allowed_hosts()

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

        super().setup()

    @classmethod
    def setup_allowed_hosts(cls) -> None:
        """Configure Django ALLOWED_HOSTS variable from environment."""
        if "ALLOWED_HOST" in os.environ:
            allowed_host = os.environ["ALLOWED_HOST"]
        else:
            # TODO remove default value and make this raise a
            #  RuntimeError instead
            allowed_host = "www.projectifyapp.com"
            warnings.warn(
                "Expected ALLOWED_HOST variable in the environment."
                "Falling back to "
                f"ALLOWED_HOST={allowed_host}"
            )
        cls.ALLOWED_HOSTS = [allowed_host]
        cls.FRONTEND_URL = f"https://{allowed_host}"

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
        stripe_keys = {
            "STRIPE_PUBLISHABLE_KEY",
            "STRIPE_SECRET_KEY",
            "STRIPE_PRICE_OBJECT",
            "STRIPE_ENDPOINT_SECRET",
        }
        if all(key in credentials for key in stripe_keys):
            cls.STRIPE_CONFIG = StripeConfig(
                STRIPE_PUBLISHABLE_KEY=credentials["STRIPE_PUBLISHABLE_KEY"],
                STRIPE_SECRET_KEY=credentials["STRIPE_SECRET_KEY"],
                STRIPE_PRICE_OBJECT=credentials["STRIPE_PRICE_OBJECT"],
                STRIPE_ENDPOINT_SECRET=credentials["STRIPE_ENDPOINT_SECRET"],
            )
        else:
            raise RuntimeError(
                f"You must specify the following Stripe configuration "
                f"in {credentials_file}:\n"
                f"{', '.join(stripe_keys)}"
            )

    @classmethod
    def setup_allauth(
        cls, credentials_file: Path, credentials: dict[str, Any]
    ) -> None:
        """Load allauth configuration."""
        github_keys = {"ALLAUTH_GITHUB_CLIENT_ID", "ALLAUTH_GITHUB_SECRET"}
        if all(key in credentials for key in github_keys):
            cls.SOCIALACCOUNT_PROVIDERS["github"]["APPS"].append(
                {
                    "client_id": credentials["ALLAUTH_GITHUB_CLIENT_ID"],
                    "secret": credentials["ALLAUTH_GITHUB_SECRET"],
                }
            )
        else:
            raise RuntimeError(
                f"You must specify the following Google OAuth credentials "
                f"in {credentials_file}:\n"
                f"{', '.join(github_keys)}"
            )

        google_keys = {"ALLAUTH_GOOGLE_CLIENT_ID", "ALLAUTH_GOOGLE_SECRET"}
        if all(key in credentials for key in google_keys):
            cls.SOCIALACCOUNT_PROVIDERS["google"]["APPS"].append(
                {
                    "client_id": credentials["ALLAUTH_GOOGLE_CLIENT_ID"],
                    "secret": credentials["ALLAUTH_GOOGLE_SECRET"],
                }
            )
        else:
            raise RuntimeError(
                f"You must specify the following Google OAuth credentials "
                f"in {credentials_file}:\n"
                f"{', '.join(google_keys)}"
            )

        apple_keys = {
            "ALLAUTH_APPLE_CLIENT_ID",
            "ALLAUTH_APPLE_SECRET",
            "ALLAUTH_APPLE_KEY",
            "ALLAUTH_APPLE_CERTIFICATE_KEY",
        }
        # TODO make log in with apple NOT optional
        if all(key in credentials for key in apple_keys):
            cls.SOCIALACCOUNT_PROVIDERS["apple"]["APPS"].append(
                {
                    "client_id": credentials["ALLAUTH_APPLE_CLIENT_ID"],
                    "secret": credentials["ALLAUTH_APPLE_SECRET"],
                    "key": credentials["ALLAUTH_APPLE_KEY"],
                    "settings": {
                        "certificate_key": credentials[
                            "ALLAUTH_APPLE_CERTIFICATE_KEY"
                        ]
                    },
                }
            )
        else:
            warnings.warn(
                "Launching Projectify without Apple OAuth credentials. "
                f"You must specify the following keys in {credentials_file}:\n"
                f"{', '.join(apple_keys)} to enable Apple OAuth"
            )

    @classmethod
    def setup_email(
        cls, credentials_file: Path, credentials: dict[str, Any]
    ) -> None:
        """Load SMTP mail configuration."""
        keys = "EMAIL_HOST", "EMAIL_HOST_USER", "EMAIL_HOST_PASSWORD"
        if all(key in credentials for key in keys):
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

        email_keys = {"ADMIN_NAME", "ADMIN_EMAIL"}
        if all(key in credentials for key in email_keys):
            cls.ADMINS = [
                [credentials["ADMIN_NAME"], credentials["ADMIN_EMAIL"]]
            ]
        else:
            raise RuntimeError(
                f"You must specify the following admin email configuration variables"
                f"in {credentials_file}:\n"
                f"{', '.join(email_keys)}"
            )

        if "DEFAULT_FROM_EMAIL" in credentials:
            cls.DEFAULT_FROM_EMAIL = credentials["DEFAULT_FROM_EMAIL"]
            cls.SERVER_EMAIL = cls.DEFAULT_FROM_EMAIL
        else:
            warnings.warn(
                f"You need to set DEFAULT_FROM_EMAIL in {credentials_file}\n"
                "Not setting DEFAULT_FROM_EMAIL and SERVER_EMAIL"
            )

    @classmethod
    def post_setup(cls) -> None:
        """Warn if ADMINS is empty."""
        super().post_setup()
        if len(cls.ADMINS) == 0:
            warnings.warn(
                "No admin contacts set up. Set the ADMIN_EMAILS environment variable."
            )
