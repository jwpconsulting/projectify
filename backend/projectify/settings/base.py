# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2021-2024 JWP Consulting GK
"""
Django settings for projectify project.

Generated by 'django-admin startproject' using Django 3.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import os
import warnings
from collections.abc import (
    Sequence,
)
from pathlib import (
    Path,
)
from typing import Optional

import dj_database_url
from configurations.base import (
    Configuration,
)

from .monkeypatch import (
    patch,
)
from .types import (
    ChannelLayers,
    StoragesConfig,
    TemplatesConfig,
)

patch()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


class Base(Configuration):
    """
    Base configuration.

    Largely derived from Django quick-start development settings - unsuitable
    for production.

    See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/
    """

    # Used in admin site to show which environment we are using
    SITE_TITLE: Optional[str] = None

    # SECURITY WARNING: don't run with debug turned on in production!
    ALLOWED_HOSTS: Sequence[str] = []

    # Debug
    DEBUG_TOOLBAR = False
    DEBUG = False

    FRONTEND_URL: str

    SESSION_COOKIE_SAMESITE = "Strict"
    SESSION_COOKIE_SECURE = True

    # CSRF
    CSRF_USE_SESSIONS = False
    CSRF_COOKIE_SAMESITE = "Strict"
    CSRF_COOKIE_SECURE = True
    CSRF_TRUSTED_ORIGINS: Optional[Sequence[str]]

    # CORS
    CORS_ALLOW_CREDENTIALS = True
    CORS_ALLOWED_ORIGINS: Optional[Sequence[str]]

    # HSTS
    SECURE_HSTS_SECONDS = 3600
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

    # Installed applications
    # Applications from Django project
    INSTALLED_APPS_DJANGO = (
        "channels",
        "daphne",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
    )

    # Any third party applications we are using
    # It's wise to reduce our dependency on third party dependencies as much as
    # we can, while avoiding to reinvent the wheel every time.
    INSTALLED_APPS_THIRD_PARTY = (
        "cloudinary",
        "cloudinary_storage",
        "django_celery_results",
        "rest_framework",
        "rules.apps.AutodiscoverRulesConfig",
        "pgtrigger",
    )

    INSTALLED_APPS_FIRST_PARTY = (
        # TODO check if this can be alphabetized
        # Replaces 'django.contrib.admin'
        "projectify.admin.apps.ProjectifyAdminConfig",
        "projectify",
        "projectify.user.apps.UserConfig",
        "projectify.workspace.apps.WorkspaceConfig",
        "projectify.corporate.apps.CorporateConfig",
        "projectify.premail",
    )

    INSTALLED_APPS: Sequence[str] = (
        INSTALLED_APPS_DJANGO
        + INSTALLED_APPS_THIRD_PARTY
        + INSTALLED_APPS_FIRST_PARTY
    )

    MIDDLEWARE = [
        "django.middleware.security.SecurityMiddleware",
        "projectify.middleware.reverse_proxy",
        "django.middleware.gzip.GZipMiddleware",
        "corsheaders.middleware.CorsMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
    ]

    ROOT_URLCONF = "projectify.urls"

    WSGI_APPLICATION = "projectify.wsgi.application"
    ASGI_APPLICATION = "projectify.asgi.application"

    # Channels
    CHANNEL_LAYERS: ChannelLayers = {
        "default": {
            "BACKEND": "channels.layers.InMemoryChannelLayer",
        },
    }

    # Database
    # https://docs.djangoproject.com/en/3.2/ref/settings/#databases
    DATABASES: dict[str, dj_database_url.DBConfig]
    # There was a reason why we added this - some weird issue
    # with channels timing out. I am commenting this out temporarily.
    # DATABASES["default"]["OPTIONS"] = {
    #     "options": (
    #         "-c statement_timeout=5000 "
    #         "-c lock_timeout=5000 "
    #         "-c idle_in_transaction_session_timeout=5000 "
    #     ),
    # }

    @classmethod
    def setup(cls) -> None:
        """Load database config, after environment is correctly loaded."""
        CONN_MAX_AGE = 0
        cls.DATABASES = {
            "default": dj_database_url.config(conn_max_age=CONN_MAX_AGE)
        }

    # Password validation
    # https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators
    AUTH_PASSWORD_VALIDATORS = [
        {
            "NAME": "django.contrib.auth.password_validation."
            "UserAttributeSimilarityValidator",
        },
        {
            "NAME": "django.contrib.auth.password_validation."
            "MinimumLengthValidator",
        },
        {
            "NAME": "django.contrib.auth.password_validation."
            "CommonPasswordValidator",
        },
        {
            "NAME": "django.contrib.auth.password_validation."
            "NumericPasswordValidator",
        },
    ]

    # Authentication
    AUTHENTICATION_BACKENDS = (
        "rules.permissions.ObjectPermissionBackend",
        "django.contrib.auth.backends.ModelBackend",
    )

    # Internationalization
    # https://docs.djangoproject.com/en/3.2/topics/i18n/
    LANGUAGE_CODE = "en-us"

    TIME_ZONE = "UTC"

    USE_I18N = True

    USE_TZ = True

    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/3.2/howto/static-files/
    STATIC_URL = "/static/django/"
    STATIC_ROOT = Path(BASE_DIR, "staticfiles")

    # Default primary key field type
    # https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field
    DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

    AUTH_USER_MODEL = "user.User"

    TEMPLATES: TemplatesConfig = [
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "APP_DIRS": True,
            "OPTIONS": {
                "context_processors": (
                    "projectify.context_processors.frontend_url",
                    "django.template.context_processors.debug",
                    "django.template.context_processors.request",
                    "django.contrib.auth.context_processors.auth",
                    "django.contrib.messages.context_processors.messages",
                ),
            },
        }
    ]

    # Celery
    CELERY_TIMEZONE = "Asia/Tokyo"
    CELERY_TASK_TRACK_STARTED = True
    CELERY_TASK_TIME_LIMIT = 30 * 60
    CELERY_RESULT_BACKEND = "django-db"
    CELERY_BROKER_URL: Optional[str] = None

    # Email
    DEFAULT_FROM_EMAIL = '"Projectify" <hello@projectifyapp.com>'
    EMAIL_EAGER = False

    # Rest framework
    REST_FRAMEWORK = {
        "DEFAULT_AUTHENTICATION_CLASSES": [
            "rest_framework.authentication.SessionAuthentication",
        ],
        "DEFAULT_PERMISSION_CLASSES": (
            "rest_framework.permissions.IsAuthenticated",
        ),
        "EXCEPTION_HANDLER": "projectify.lib.exception_handler.exception_handler",
        "NON_FIELD_ERRORS_KEY": "drf_general",
    }

    # Where to store media
    MEDIA_ROOT = BASE_DIR / "media"
    MEDIA_URL = "/media/"
    SERVE_MEDIA = False

    # Logging
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "like_gunicorn": {
                "format": "%(levelname)-s [%(module)s] ~ %(message)s",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "like_gunicorn",
            },
        },
        "loggers": {
            "": {
                "handlers": ["console"],
                "level": os.getenv("DJANGO_LOG_LEVEL", "INFO"),
            },
        },
    }

    # Cloudinary
    MEDIA_CLOUDINARY_STORAGE = (
        "cloudinary_storage.storage.MediaCloudinaryStorage"
    )
    STORAGES: StoragesConfig = {
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
        },
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        },
    }

    # Stripe
    STRIPE_SECRET_KEY: Optional[str] = None
    STRIPE_ENDPOINT_SECRET: Optional[str] = None
    STRIPE_PRICE_OBJECT: Optional[str] = None

    # django-ratelimit
    RATELIMIT_ENABLE = True
    RATELIMIT_EXCEPTION_CLASS = "rest_framework.exceptions.Throttled"

    # drf-spectacular
    SERVE_SPECTACULAR = False

    # premail
    PREMAIL_PREVIEW = False

    # simulate slow and unreliable connections
    SLEEP_MIN_MAX_MS: Optional[tuple[int, int]] = None
    # Percentage (int from 0 to 100) of requests that should fail
    ERROR_RATE_PCT: Optional[int] = None
    # N seconds after which 100% of requests time out
    CHANNEL_ERROR: Optional[int] = None

    @classmethod
    def post_setup(cls) -> None:
        """Warn if FRONTEND_URL ends on '/'."""
        # Technically, this won't catch multiple trailing slashes... but who
        # would specify a URL like that?
        if not cls.FRONTEND_URL.endswith("/"):
            return
        warnings.warn("Please ensure FRONTEND_URL does not end on a '/'")
        cls.FRONTEND_URL = cls.FRONTEND_URL[:-1]
