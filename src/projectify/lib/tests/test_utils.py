# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2026 JWP Consulting GK
"""Test Projectify lib utils."""

from typing import Optional

import pytest

from ..utils import clean_rich_text, static_image_get_with_dimensions


@pytest.mark.parametrize(
    "html,expected",
    [
        ("<p>alert('hello-world')</p>", "<p>alert('hello-world')</p>"),
        ("<p><script>alert('hello-world')</script></p>", "<p></p>"),
        ("<p>&<></p>", "<p>&amp;&lt;&gt;</p>"),
        ('<a href="#">bla asd</a>', '<a href="#">bla asd</a>'),
    ],
)
def test_clean_rich_text(html: str, expected: Optional[str]) -> None:
    """Test rich text cleaning."""
    assert clean_rich_text(html) == expected


def test_static_image_get_with_dimensions() -> None:
    """Test getting image dimensions."""
    result = static_image_get_with_dimensions("apple-touch-icon.png")

    assert result is not None
    url, width, height = result
    # This magically returns us a webp file
    assert "apple-touch-icon.webp" in url
    assert width == 180
    assert height == 180
