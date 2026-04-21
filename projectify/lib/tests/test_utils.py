# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2026 JWP Consulting GK
"""Test Projectify lib utils."""

from typing import Optional

import pytest

from ..utils import (
    extract_first_paragraph_text,
    static_image_get_with_dimensions,
)


@pytest.mark.parametrize(
    "html,expected",
    [
        ("Hello world", "Hello world"),
        ("<p>Hello world</p>", "Hello world"),
        ("<p>First</p><p>Second</p>", "First"),
        ("<div><p>Nested</p></div>", "Nested"),
        ("<p>  whitespace  </p>", "whitespace"),
        ("<p></p>", None),
        ("", None),
        ("<div>no paragraph here</div><p>But here</p>", "But here"),
        (
            "<div>Counts as a paragraph if no other tag exists</div>",
            "Counts as a paragraph if no other tag exists",
        ),
        (
            "<p>Multiple <strong>tags</strong> inside</p>",
            "Multiple tags inside",
        ),
        ("<h1>Heading</h1><p>After heading</p>", "After heading"),
        # Adversarial examples
        # Unclosed tag
        ("<p>  whitespace ", "whitespace"),
        # Script tag
        ("<p><script>alert('xss')</script></p>", "alert('xss')"),
        # Empty paragraphs are skipped; the first non-empty one is returned
        ("<p></p><p>Second non-empty</p>", "Second non-empty"),
        # Multiple empty paragraphs before a non-empty one
        ("<p></p><p>  </p><p>Third non-empty</p>", "Third non-empty"),
        # HTML entities
        ("<p>&amp;&lt;&gt;</p>", "&<>"),
    ],
)
def test_extract_first_paragraph_text(
    html: str, expected: Optional[str]
) -> None:
    """Test extracting plain text from the first paragraph."""
    assert extract_first_paragraph_text(html) == expected


def test_static_image_get_with_dimensions() -> None:
    """Test getting image dimensions."""
    result = static_image_get_with_dimensions("apple-touch-icon.png")

    assert result is not None
    url, width, height = result
    # This magically returns us a webp file
    assert "apple-touch-icon.webp" in url
    assert width == 180
    assert height == 180
