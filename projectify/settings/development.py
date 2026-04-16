# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2021-2026 JWP Consulting GK
"""Development settings."""

import os
import warnings
from collections.abc import Iterable, Sequence

import dj_database_url

from .types import StripeConfig

try:
    from dotenv import load_dotenv
except ImportError as e:
    raise RuntimeError(
        "dotenv was not found. Please check if dev dependencies have been installed"
    ) from e

from .base import Base


def add_dev_middleware(
    middleware: Sequence[str], debug_toolbar: bool, browser_reload: bool
) -> Iterable[str]:
    """
    Add the debug and reload middleware after the gzip mdware.

    Control with `debug_toolbar` and `browser_reload`.
    """
    gzip_middleware = "django.middleware.gzip.GZipMiddleware"
    for m in middleware:
        if m == gzip_middleware:
            yield m
            if debug_toolbar:
                yield "debug_toolbar.middleware.DebugToolbarMiddleware"
            if browser_reload:
                yield "django_browser_reload.middleware.BrowserReloadMiddleware"
        else:
            yield m


class Development(Base):
    """Development configuration."""

    SITE_TITLE = "Local Development"

    SECRET_KEY = "development"

    INSTALLED_APPS: Sequence[str] = (
        *Base.INSTALLED_APPS,
        "django_browser_reload",
        "django_extensions",
        # For testing allauth connection
        "allauth.socialaccount.providers.openid_connect",
    )

    # Debug
    DEBUG = True
    DEBUG_TOOLBAR = True
    DEBUG_AUTH = True
    DEBUG_ERROR_PAGES = True

    ALLOWED_HOSTS = os.getenv(
        "ALLOWED_HOSTS", ".localhost,127.0.0.1,[::1]"
    ).split(",")
    # Add the IP you are connecting from to get SQL debug HTTP headers
    INTERNAL_IPS = os.getenv("INTERNAL_IPS", "127.0.0.1").split(",")

    # XXX while developing the new frontend, this is set to
    # match Django's ./manage.py runserver port
    FRONTEND_URL = "http://localhost:8000"

    # CSRF Cookie settings
    # ====================
    # Needed for Safari, since it refuses to set cookies when
    # receiving them from localhost, see:
    # https://github.com/lucia-auth/lucia/discussions/1755#discussioncomment-11496827
    # and
    # draft-ietf-httpbis-rfc6265bis-latest
    # https://httpwg.org/http-extensions/draft-ietf-httpbis-rfc6265bis.html#name-top-level-requests-with-uns
    # > 4.1.2.5. The Secure Attribute
    # > The Secure attribute limits the scope of the cookie to "secure"
    # channels (where "secure" is defined by the user agent). […]
    CSRF_COOKIE_SECURE = False

    # Email
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
    SERVER_EMAIL = "hello@projectifyapp.com"

    # Media
    SENDFILE_BACKEND = "django_sendfile.backends.simple"

    # Safari workaround for sessionid cookie
    SESSION_COOKIE_SECURE = False
    # TODO remove after Svelte frontend is gone
    SESSION_COOKIE_SAMESITE = "Lax"

    # Admins for local logging
    ADMINS = [["Local user", "user@localhost"]]

    # Show preview of all email types
    PREMAIL_PREVIEW = True

    # Enable live reloading
    BROWSER_RELOAD = True

    # Enable template debugging
    TEMPLATES = Base.TEMPLATES
    TEMPLATES[0]["OPTIONS"] = {**TEMPLATES[0]["OPTIONS"], "debug": True}

    # Logging with timestamps for development
    LOGGING = {
        **Base.LOGGING,
        "formatters": {
            "like_gunicorn": {
                "format": "[%(asctime)s] %(levelname)-s [%(name)s.%(module)s] ~ %(message)s",
                "datefmt": "%d/%b/%Y %H:%M:%S",
            }
        },
        "loggers": {
            **Base.LOGGING["loggers"],
            "django": {"handlers": ["console"], "propagate": False},
        },
    }

    @classmethod
    def pre_setup(cls) -> None:
        """Load environment variables from .env."""
        super().pre_setup()
        load_dotenv()

    @classmethod
    def setup(cls) -> None:
        """Enable debug toolbar."""
        super().setup()
        if cls.DEBUG_TOOLBAR:
            cls.INSTALLED_APPS = (*cls.INSTALLED_APPS, "debug_toolbar")
        cls.MIDDLEWARE = list(
            add_dev_middleware(
                Base.MIDDLEWARE, cls.DEBUG_TOOLBAR, cls.BROWSER_RELOAD
            )
        )

        # Add CSP report URI for development
        cls.SECURE_CSP = {**Base.SECURE_CSP, "report-uri": ["/csp-report/"]}
        cls.DATABASES["default"] = dj_database_url.config(
            default="sqlite:///projectify.sqlite",
            conn_max_age=cls.CONN_MAX_AGE,
        )

        # Allauth mock app, GitHub OAuth, and Google OAuth settings
        cls.SOCIALACCOUNT_PROVIDERS["openid_connect"] = {
            "APPS": [
                {
                    "provider_id": "local-test",
                    "client_id": "test.id",
                    "secret": "secret",
                    # TODO define server_url
                }
            ]
        }
        cls.configure_github_oauth()
        cls.configure_google_oauth()
        cls.configure_stripe()

    @classmethod
    def configure_github_oauth(cls) -> None:
        """Check for GitHub OAuth config and apply if present."""
        keys = "ALLAUTH_GITHUB_CLIENT_ID", "ALLAUTH_GITHUB_SECRET"
        keys_present = all(key in os.environ for key in keys)
        if not keys_present:
            names = ", ".join(keys)
            warnings.warn(
                "To test GitHub OAuth in the local development environment, "
                f"you must set the following environment variables: {names}"
            )
            return
        cls.SOCIALACCOUNT_PROVIDERS["github"]["APPS"].append(
            {
                "client_id": os.environ["ALLAUTH_GITHUB_CLIENT_ID"],
                "secret": os.environ["ALLAUTH_GITHUB_SECRET"],
            }
        )

    @classmethod
    def configure_google_oauth(cls) -> None:
        """Check for Google OAuth config and apply if present."""
        keys = "ALLAUTH_GOOGLE_CLIENT_ID", "ALLAUTH_GOOGLE_SECRET"
        keys_present = all(key in os.environ for key in keys)
        if not keys_present:
            names = ", ".join(keys)
            warnings.warn(
                "To test Google OAuth in the local development environment, "
                f"you must set the following environment variables: {names}"
            )
            return
        cls.SOCIALACCOUNT_PROVIDERS["google"]["APPS"].append(
            {
                "client_id": os.environ["ALLAUTH_GOOGLE_CLIENT_ID"],
                "secret": os.environ["ALLAUTH_GOOGLE_SECRET"],
            }
        )

    @classmethod
    def configure_stripe(cls) -> None:
        """Check for Stripe environment variables."""
        required_keys = [
            "STRIPE_PUBLISHABLE_KEY",
            "STRIPE_SECRET_KEY",
            "STRIPE_ENDPOINT_SECRET",
            "STRIPE_PRICE_OBJECT",
        ]
        configuration_keys_present = all(
            key in os.environ for key in required_keys
        )
        if not configuration_keys_present:
            names = ", ".join(required_keys)
            warnings.warn(
                "To test the stripe integration in the local development environment, you "
                f"must pass the following environment variables: {names}"
            )
            return

        cls.STRIPE_CONFIG = StripeConfig(
            STRIPE_PUBLISHABLE_KEY=os.environ["STRIPE_PUBLISHABLE_KEY"],
            STRIPE_SECRET_KEY=os.environ["STRIPE_SECRET_KEY"],
            STRIPE_PRICE_OBJECT=os.environ["STRIPE_PRICE_OBJECT"],
            STRIPE_ENDPOINT_SECRET=os.environ["STRIPE_ENDPOINT_SECRET"],
        )
