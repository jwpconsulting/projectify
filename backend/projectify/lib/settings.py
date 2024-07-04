# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Copyright (C) 2024 JWP Consulting GK
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
"""Settings related functions."""

import os
from collections.abc import Iterable, Sequence
from typing import cast

from django.conf import settings

from projectify.settings.base import Base


def get_settings() -> Base:
    """
    Return typed settings. Uses casting, so buyer beware.

    Still better than hoping that Django settings will contain our settings.
    """
    return cast(Base, settings)


def populate_production_middleware(middleware: Sequence[str]) -> Iterable[str]:
    """Remove CORS middleware. No idea why we should do that."""
    csrf_middleware = "django.middleware.csrf.CsrfViewMiddleware"
    gzip_middleware = "django.middleware.gzip.GZipMiddleware"
    disable_csrf = "DISABLE_CSRF_PROTECTION" in os.environ
    for m in middleware:
        if m == csrf_middleware and disable_csrf:
            yield "projectify.middleware.DisableCSRFMiddleware"
            continue
        elif m == gzip_middleware:
            # Yield white noise *after* gzip
            yield m
            yield "whitenoise.middleware.WhiteNoiseMiddleware"
        else:
            yield m
