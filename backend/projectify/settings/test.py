# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Copyright (C) 2021, 2022, 2023 JWP Consulting GK
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""Test settings."""

try:
    from dotenv import load_dotenv
except ImportError as e:
    raise RuntimeError(
        "dotenv was not found. Please check if dev dependencies have been installed"
    ) from e

from .base import Base
from .spectacular import SpectacularSettings


class Test(SpectacularSettings, Base):
    """Test configuration."""

    INSTALLED_APPS = (
        *Base.INSTALLED_APPS,
        "drf_spectacular",
    )

    SITE_TITLE = "Projectify Pytest"

    # TODO populate me
    SECRET_KEY = "test"

    # Allow localhost, so that websocket connections may pass
    CSRF_TRUSTED_ORIGINS = ("http://localhost",)

    FRONTEND_URL = "https://example.com"

    # Email
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
    EMAIL_EAGER = True

    # Celery
    CELERY_BROKER_URL = "memory://"

    # django-ratelimit
    RATELIMIT_ENABLE = False

    @classmethod
    def pre_setup(cls) -> None:
        """Load environment variables from .env."""
        super().pre_setup()
        load_dotenv()


class TestCollectstatic(Test):
    """Settings to test static file collection needed for whitenoise."""

    STORAGES = {
        **Base.STORAGES,
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
        },
    }


class TestRedis(Test):
    """
    Settings used to test the connection to Redis on localhost.

    See bin/test_redis.sh
    """

    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels_redis.core.RedisChannelLayer",
            "CONFIG": {
                "hosts": [("127.0.0.1", 6379)],
            },
        },
    }
