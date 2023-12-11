"""Projectify utils."""
from typing import (
    TYPE_CHECKING,
    Optional,
)

from django.conf import (
    settings,
)

from cloudinary import (
    CloudinaryImage,
)

if TYPE_CHECKING:
    from django.db.models import FieldFile  # noqa: F401


def crop_image(
    image: Optional["FieldFile"], width: int, height: int, **kwargs: object
) -> Optional[str]:
    """Crop an image using cloudinary's API, if available."""
    if not image:
        return None
    backend = settings.STORAGES["default"]["BACKEND"]
    if backend != settings.MEDIA_CLOUDINARY_STORAGE:
        return image.url
    cloudinary_image = CloudinaryImage(image.name)
    url: str = cloudinary_image.build_url(
        width=width,
        height=height,
        crop="thumb",
        gravity="face",
        secure=True,
        **kwargs,
    )
    return url
