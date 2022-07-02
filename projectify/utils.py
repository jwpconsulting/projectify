"""Projectify utils."""
from django.conf import (
    settings,
)

from cloudinary import (
    CloudinaryImage,
)


def crop_image(image, width, height, **kwargs):
    """Crop an image using cloudinary's API, if available."""
    if not image:
        return
    if settings.DEFAULT_FILE_STORAGE != settings.MEDIA_CLOUDINARY_STORAGE:
        return image.url
    cloudinary_image = CloudinaryImage(image.name)
    url = cloudinary_image.build_url(
        width=width,
        height=height,
        crop="thumb",
        gravity="face",
        secure=True,
        **kwargs,
    )
    return url
