# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Copyright (C) 2021-2024 JWP Consulting GK
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
"""Nix development settings."""

import os
from pathlib import Path

from projectify.lib.settings import populate_production_middleware
from projectify.settings.base import Base

from .development import Development


class DevelopmentNix(Development):
    """Preliminary configuration for poetry2nix packaged backend."""

    SITE_TITLE = "Projectify-Backend (nix)"

    STORAGES = {
        **Development.STORAGES,
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
        },
    }

    # Use middelware from production for added realism
    MIDDLEWARE = list(populate_production_middleware(Base.MIDDLEWARE))

    # We need to inject the static root path during the nix build process
    STATIC_ROOT = Path(os.environ["STATIC_ROOT"])
    STATIC_URL = "/backend/static/"

    # No need for debug or debug libs, for added realism
    DEBUG = False
    INSTALLED_APPS = Base.INSTALLED_APPS
    SERVE_SPECTACULAR = False
    DEBUG_TOOLBAR = False
