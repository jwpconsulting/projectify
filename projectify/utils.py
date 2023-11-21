"""Projectify utils."""
from typing import (
    TYPE_CHECKING,
    Optional,
    Type,
    cast,
)

from django.conf import (
    settings,
)
from django.contrib.auth import get_user_model as _get_user_model
from django.contrib.auth.models import (
    AbstractBaseUser,
)

from cloudinary import (
    CloudinaryImage,
)

if TYPE_CHECKING:
    from django.db.models import FieldFile  # noqa: F401

    from user.models import User as _User


# TODO
# Use this everywhere, refactor to some util module
def get_user_model() -> Type["_User"]:
    """Return a correctly typed user model."""
    abstract_base_user: Type[AbstractBaseUser] = _get_user_model()
    return cast(Type["_User"], abstract_base_user)


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
