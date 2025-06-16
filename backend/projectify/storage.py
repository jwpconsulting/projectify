# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2022-2024 JWP Consulting GK
"""Storage classes."""

from urllib.parse import urljoin

from django.core.files.storage import FileSystemStorage
from django.utils.functional import cached_property

from projectify.lib.settings import get_settings


class LocalhostStorage(FileSystemStorage):
    """Override file system storage."""

    @cached_property
    def base_url(self) -> str:  # type: ignore
        """Override base url to point to localhost."""
        settings = get_settings()
        if not settings.FRONTEND_URL:
            raise ValueError("Need to set FRONTEND_URL to determine base_url")
        url: str = urljoin(settings.FRONTEND_URL, settings.MEDIA_URL)
        return url
