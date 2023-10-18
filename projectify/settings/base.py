"""
Django settings for projectify project.

Generated by 'django-admin startproject' using Django 3.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os
from collections.abc import (
    Sequence,
)
from pathlib import (
    Path,
)
from typing import (
    Iterable,
)

import dj_database_url
from configurations.base import (
    Configuration,
)
from dotenv import (
    load_dotenv,
)

from .monkeypatch import (
    patch,
)
from .types import (
    ChannelLayers,
    StoragesConfig,
    TemplatesConfig,
)


load_dotenv()

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

    # SECURITY WARNING: don't run with debug turned on in production!
    ALLOWED_HOSTS: Iterable[str] = []

    SESSION_COOKIE_SAMESITE = "None"
    SESSION_COOKIE_SECURE = True

    # CSRF
    CSRF_USE_SESSIONS = False
    CSRF_COOKIE_SAMESITE = "None"
    CSRF_COOKIE_SECURE = True

    # CORS
    CORS_ALLOW_CREDENTIALS = True

    # Installed applications
    # Applications from Django project
    INSTALLED_APPS_DJANGO = (
        "channels",
        "daphne",
        "django.contrib.admin",
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
        "django_extensions",
        # TODO
        # We don't want to use GraphQL anymore.
        "strawberry.django",
        # XXX are we still using this?
        "ordered_model",
        # TODO I think this is ours, not third party
        "premail",
        "rest_framework",
        "rules.apps.AutodiscoverRulesConfig",
        "pgtrigger",
    )

    INSTALLED_APPS_FIRST_PARTY = (
        # TODO check if this can be alphabetized
        "projectify",
        "user",
        "workspace",
        "blog",
        "corporate",
    )

    INSTALLED_APPS: Sequence[str] = (
        INSTALLED_APPS_DJANGO
        + INSTALLED_APPS_THIRD_PARTY
        + INSTALLED_APPS_FIRST_PARTY
    )

    MIDDLEWARE = [
        "django.middleware.security.SecurityMiddleware",
        "django.middleware.gzip.GZipMiddleware",
        # TODO white noise middleware is only needed in production
        "whitenoise.middleware.WhiteNoiseMiddleware",
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
    CONN_MAX_AGE = 0
    # TODO inject OPTIONS cleanly when calling .config()
    DATABASES = {"default": dj_database_url.config(conn_max_age=CONN_MAX_AGE)}
    DATABASES["default"]["OPTIONS"] = {
        "options": (
            "-c statement_timeout=5000 "
            "-c lock_timeout=5000 "
            "-c idle_in_transaction_session_timeout=5000 "
        ),
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
    STATIC_URL = "/static/"
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

    # Email
    DEFAULT_FROM_EMAIL = "hello@projectifyapp.com"
    EMAIL_EAGER = False

    # Rest framework
    REST_FRAMEWORK = {
        "DEFAULT_AUTHENTICATION_CLASSES": [
            "rest_framework.authentication.SessionAuthentication",
        ],
        "DEFAULT_PERMISSION_CLASSES": (
            "rest_framework.permissions.IsAuthenticated",
        ),
    }

    # Where to store media
    MEDIA_ROOT = BASE_DIR / "media"
    MEDIA_URL = "/media/"
    SERVE_MEDIA = False

    # Logging
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
            },
        },
        "root": {
            "handlers": ["console"],
            "level": os.getenv("DJANGO_LOG_LEVEL", "INFO"),
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

    # Debug
    DEBUG_TOOLBAR = False
    DEBUG = False
