# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2026 JWP Consulting GK
"""Test Projectify lib utils."""

from ..utils import static_image_get_with_dimensions


def test_static_image_get_with_dimensions() -> None:
    """Test getting image dimensions."""
    result = static_image_get_with_dimensions("apple-touch-icon.png")

    assert result is not None
    url, width, height = result
    assert "apple-touch-icon.png" in url
    assert width == 180
    assert height == 180
