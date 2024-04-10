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
"""DRF-Spectacular settings."""


class SpectacularSettings:
    """Settings mixin used for drf-spectacular."""

    # drf-spectacular
    # from
    # https://drf-spectacular.readthedocs.io/en/latest/readme.html#installation
    SPECTACULAR_SETTINGS = {
        "TITLE": "Projectify backend API",
        "DESCRIPTION": "API for the Projectify project management software",
        "VERSION": "1.0.0",
        "SERVE_INCLUDE_SCHEMA": False,
    }
