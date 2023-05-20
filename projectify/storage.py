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
