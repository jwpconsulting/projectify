# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2021-2024 JWP Consulting GK
"""Development settings."""

import os
from collections.abc import Iterable, Sequence

import dj_database_url

try:
    from dotenv import load_dotenv
except ImportError as e:
    raise RuntimeError(
        "dotenv was not found. Please check if dev dependencies have been installed"
    ) from e

from .base import Base, environ_get_or_warn


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

    # Stripe
    STRIPE_PUBLISHABLE_KEY = environ_get_or_warn("STRIPE_PUBLISHABLE_KEY")
    STRIPE_SECRET_KEY = environ_get_or_warn("STRIPE_SECRET_KEY")
    STRIPE_PRICE_OBJECT = environ_get_or_warn("STRIPE_PRICE_OBJECT")
    STRIPE_ENDPOINT_SECRET = environ_get_or_warn("STRIPE_ENDPOINT_SECRET")

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
    TEMPLATES[0]["OPTIONS"] = {
        **TEMPLATES[0]["OPTIONS"],
        "debug": True,
    }

    # Logging with timestamps for development
    LOGGING = {
        **Base.LOGGING,
        "formatters": {
            "like_gunicorn": {
                "format": "[%(asctime)s] %(levelname)-s [%(name)s.%(module)s] ~ %(message)s",
                "datefmt": "%d/%b/%Y %H:%M:%S",
            },
        },
        "loggers": {
            **Base.LOGGING["loggers"],
            "django": {
                "handlers": ["console"],
                "propagate": False,
            },
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
        cls.SECURE_CSP = {
            **Base.SECURE_CSP,
            "report-uri": ["/csp-report/"],
        }
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
                }
            ]
        }
        cls.SOCIALACCOUNT_PROVIDERS["github"]["APPS"].append(
            {
                "client_id": environ_get_or_warn(
                    "ALLAUTH_GITHUB_CLIENT_ID",
                    "You need to set this environment variable for logging in with GitHub.",
                ),
                "secret": environ_get_or_warn(
                    "ALLAUTH_GITHUB_SECRET",
                    "You need to set this environment variable for logging in with Github.",
                ),
            }
        )

        cls.SOCIALACCOUNT_PROVIDERS["google"]["APPS"].append(
            {
                "client_id": environ_get_or_warn(
                    "ALLAUTH_GOOGLE_CLIENT_ID",
                    "You need to set this environment variable to enable log in with Google",
                ),
                "secret": environ_get_or_warn(
                    "ALLAUTH_GOOGLE_SECRET",
                    "You need to set this environment variable to enable log in with Google",
                ),
            }
        )
