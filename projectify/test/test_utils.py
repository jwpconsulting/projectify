"""Test projectify utils."""
import os
from typing import (
    TYPE_CHECKING,
    Any,
)
from unittest import (
    mock,
)

import pytest

from .. import (
    utils,
)


if TYPE_CHECKING:
    from django.db.models import (
        FieldFile,
    )


class TestCropImage:
    """Test crop_image."""

    @pytest.fixture
    def image(self) -> "FieldFile":
        """Image fixture."""
        image = mock.MagicMock()
        image.name = "hello_world"
        image.url = "https://www.example.com/hello_world.jpg"
        return image

    def test_with_none(self) -> None:
        """Test with nothing."""
        url = utils.crop_image(None, 100, 100)
        assert url is None

    @mock.patch.dict(os.environ, {"CLOUDINARY_URL": "https://example.com"})
    def test_with_cloudinary(
        self,
        image: "FieldFile",
        settings: Any,
    ) -> None:
        """Test with cloudinary file storage."""
        settings.DEFAULT_FILE_STORAGE = settings.MEDIA_CLOUDINARY_STORAGE
        url = utils.crop_image(image, 100, 100, cloud_name="bbbbbbbbb")
        assert url == (
            "https://res.cloudinary.com/bbbbbbbbb"
            "/image/upload/c_thumb,g_face,h_100,w_100/hello_world"
        )

    def test_with_local(self, image: "FieldFile") -> None:
        """Test with cloudinary file storage."""
        url = utils.crop_image(image, 100, 100)
        assert url == image.url
