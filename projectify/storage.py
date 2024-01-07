# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Copyright (C) 2022, 2023 JWP Consulting GK
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
"""Storage classes."""
from urllib.parse import (
    urljoin,
)

from django.conf import (
    settings,
)
from django.core.files.storage import (
    FileSystemStorage,
)
from django.utils.functional import (
    cached_property,
)


class LocalhostStorage(FileSystemStorage):
    """Override file system storage."""

    @cached_property
    def base_url(self) -> str:  # type: ignore
        """Override base url to point to localhost."""
        url: str = urljoin("http://localhost:8000", settings.MEDIA_URL)
        return url
