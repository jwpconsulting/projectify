# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2026 JWP Consulting GK
"""Test workspace app utils."""

from typing import Optional

import pytest

from ..utils import extract_first_paragraph_text, strip_first_paragraph


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
        (
            "<div>Counts as first paragraph</div><p>Second</p>",
            "Counts as first paragraph",
        ),
        (
            "<div>Counts as a paragraph if no other tag exists</div>",
            "Counts as a paragraph if no other tag exists",
        ),
        (
            "<p>Multiple <strong>tags</strong> inside</p>",
            "Multiple tags inside",
        ),
        ("<h1>Heading</h1><p>After heading</p>", "Heading"),
        # Adversarial examples
        # Unclosed tag
        ("<p>  whitespace ", "whitespace"),
        # Script tag
        ("<p>alert('hello-world')</p>", "alert('hello-world')"),
        # JustHTML drops script and style contents
        ("<p><script>alert('xss')</script>Hello</p>", "Hello"),
        ("<p><style>alert('xss')</style>CSS too</p>", "CSS too"),
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


@pytest.mark.parametrize(
    "html,expected",
    [
        ("Hello world", None),
        ("<p>Hello world</p>", None),
        ("<p>First</p><p>Second</p>", "<p>Second</p>"),
        (
            '<p>First</p><a href="#url">Second  bla   </a>',
            '<a href="#url">Second bla</a>',
        ),
        ("<div><p>Nested</p></div>", None),
        (
            "<p>Hey</p><p>  white <strong>space</strong> </p>",
            "<p>  white <strong>space</strong></p>",
        ),
        ("<p></p>", None),
        ("", None),
        ("<p>no paragraph here</p><p>But here</p>", "<p>But here</p>"),
        ("<h1>Heading</h1><p>After heading</p>", "<p>After heading</p>"),
        # Adversarial examples
        # Unclosed tag
        ("<p>hey</p><p>  whitespace ", "<p>whitespace</p>"),
        # Script tag
        (
            "<p>hey</p><p>hello <script>alert('xss')</script>world</p>",
            "<p>hello world</p>",
        ),
        # Empty paragraphs are skipped; the first non-empty one is returned
        ("<p></p><p>Second non-empty</p><p>Third</p>", "<p>Third</p>"),
        # Multiple empty paragraphs before a non-empty one
        (
            "<p></p><p>  </p><p>Third non-empty</p><p>Fourth</p>",
            "<p>Fourth</p>",
        ),
        # HTML entities
        ("<p>first</p><p>&amp;&lt;&gt;</p>", "<p>&amp;&lt;&gt;</p>"),
    ],
)
def test_strip_first_paragraph(html: str, expected: Optional[str]) -> None:
    """Test stripping the first paragraph."""
    assert strip_first_paragraph(html) == expected
