"""Test workspace schema types."""
from unittest import (
    mock,
)

import pytest

from ...schema import (
    types,
)


class TestCropImage:
    """Test crop_image."""

    @pytest.fixture
    def image(self):
        """Image fixture."""
        image = mock.MagicMock()
        image.name = "hello_world"
        image.url = "https://www.example.com/hello_world.jpg"
        return image

    def test_with_cloudinary(self, image, settings):
        """Test with cloudinary file storage."""
        settings.DEFAULT_FILE_STORAGE = settings.MEDIA_CLOUDINARY_STORAGE
        url = types.crop_image(image, 100, 100, cloud_name="bbbbbbbbb")
        assert url == (
            "http://res.cloudinary.com/bbbbbbbbb"
            "/image/upload/c_crop,g_face,h_100,w_100/hello_world"
        )

    def test_with_local(self, image):
        """Test with cloudinary file storage."""
        url = types.crop_image(image, 100, 100)
        assert url == image.url
