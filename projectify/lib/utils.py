# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2026 JWP Consulting GK
"""Projectify utils."""

import logging
from html.parser import HTMLParser
from pathlib import Path
from typing import Any, Optional, Tuple

from django.contrib.staticfiles import finders
from django.core.cache import cache
from django.templatetags import static
from django.utils.safestring import SafeString, mark_safe

import bleach
from PIL import Image

from projectify.lib.settings import get_settings

logger = logging.getLogger(__name__)


def clean_rich_text(text: str) -> SafeString:
    """Clean the text for rich text content."""
    settings = get_settings()
    tags = settings.MARKDOWNIFY["default"]["WHITELIST_TAGS"]
    attrs = settings.MARKDOWNIFY["default"]["WHITELIST_ATTRS"]
    sanitized_html: str = bleach.clean(
        text, tags=tags, attributes=attrs, strip=True
    )  # type: ignore[no-untyped-call]
    # Remember that just marking it "safe" doesn't make it safe
    # sanitized_html is safe to mark as "safe" because `bleach.clean` has
    # cleaned it.
    safe_html = mark_safe(sanitized_html)
    return safe_html


# See `projectify/lib/tests/test_utils.py` for sanitization test cases
class _FirstParagraphParser(HTMLParser):
    """Extract plain text from the first non-empty <p> tag in an HTML string."""

    def __init__(self) -> None:
        """Initialize parser state."""
        super().__init__()
        self._in_p: bool = False
        self._done: bool = False
        self._text_parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: Any) -> None:
        """Track entry into a <p> tag."""
        if tag == "p" and not self._done:
            self._in_p = True
            self._text_parts = []

    def handle_endtag(self, tag: str) -> None:
        """Track exit from a <p> tag; stop if it was non-empty."""
        if tag == "p" and self._in_p:
            self._in_p = False
            if "".join(self._text_parts).strip():
                self._done = True

    def handle_data(self, data: str) -> None:
        """Collect text data inside a <p> tag."""
        if self._in_p:
            self._text_parts.append(data)

    @property
    def first_paragraph_text(self) -> Optional[str]:
        """Return the collected text, or None if nothing was found."""
        result = "".join(self._text_parts).strip()
        return result if result else None


_BLOCK_TAGS = frozenset(
    [
        "p",
        "div",
        "h1",
        "h2",
        "h3",
        "h4",
        "h5",
        "h6",
        "blockquote",
        "ul",
        "ol",
        "li",
    ]
)


class _StripFirstParagraphParser(HTMLParser):
    """Return everything after the first non-empty <p> tag."""

    def __init__(self) -> None:
        """Initialize parser state."""
        super().__init__()
        self._in_first_p: bool = False
        self._first_p_done: bool = False
        self._first_p_text: list[str] = []
        self._remainder: list[str] = []

    def handle_starttag(self, tag: str, attrs: Any) -> None:
        """Track entry into block tags."""
        if tag in _BLOCK_TAGS and not self._first_p_done:
            self._in_first_p = True
            self._first_p_text = []
            return
        if self._first_p_done and not self._in_first_p:
            attrs_str = ""
            if attrs:
                attrs_str = " " + " ".join(
                    f'{name}="{value}"' if value is not None else name
                    for name, value in attrs
                )
            self._remainder.append(f"<{tag}{attrs_str}>")

    def handle_endtag(self, tag: str) -> None:
        """Track exit from block tags."""
        if tag in _BLOCK_TAGS and self._in_first_p:
            self._in_first_p = False
            if "".join(self._first_p_text).strip():
                self._first_p_done = True
            return
        if self._first_p_done and not self._in_first_p:
            self._remainder.append(f"</{tag}>")

    def handle_data(self, data: str) -> None:
        """Collect text data."""
        if self._in_first_p:
            self._first_p_text.append(data)
        elif self._first_p_done:
            self._remainder.append(data)

    def handle_entityref(self, name: str) -> None:
        """Handle HTML entities like &amp;."""
        if self._first_p_done and not self._in_first_p:
            self._remainder.append(f"&{name};")

    def handle_charref(self, name: str) -> None:
        """Handle numeric character references like &#39;."""
        if self._first_p_done and not self._in_first_p:
            self._remainder.append(f"&#{name};")

    @property
    def remainder(self) -> Optional[str]:
        """Return the remainder after the first paragraph, or None."""
        result = "".join(self._remainder).strip()
        return result if result else None


def extract_first_paragraph_text(html: str) -> Optional[str]:
    """Return plain text from the first <p> tag in html, or None."""
    if len(html) == 0:
        return None
    # Try extracting the contents of the first <p> tag
    sanitized_html: str = bleach.clean(
        html, strip=True, tags=["p"], attributes=[]
    )  # type: ignore[no-untyped-call]
    parser = _FirstParagraphParser()
    parser.feed(sanitized_html)
    if parser.first_paragraph_text:
        return parser.first_paragraph_text
    # If the parser couldn't find the first paragraph, return the full
    # text stripped of all tags.
    all_tags_stripped: str = bleach.clean(
        html, strip=True, tags=[], attributes=[]
    )  # type: ignore[no-untyped-call]
    if len(all_tags_stripped) == 0:
        return None
    return all_tags_stripped


def strip_first_paragraph(html: str) -> Optional[SafeString]:
    """
    Strip the first <p> or other block element <div>, <h[1-6]>.

    Return None if there's nothing after the first block.
    """
    if len(html) == 0:
        return None
    # First pass: sanitize with only block/inline tags stripped, to normalize
    # the HTML before parsing. Use strip=True to remove disallowed tags like
    # <script> rather than escaping them.
    settings = get_settings()
    tags = settings.MARKDOWNIFY["default"]["WHITELIST_TAGS"]
    attrs = settings.MARKDOWNIFY["default"]["WHITELIST_ATTRS"]
    sanitized_html: str = bleach.clean(  # type: ignore[no-untyped-call]
        html, tags=tags, attributes=attrs, strip=True
    )
    parser = _StripFirstParagraphParser()
    parser.feed(sanitized_html)
    remainder = parser.remainder
    if not remainder:
        return None
    # Second pass: re-sanitize the remainder to ensure it's clean
    remainder_safe: str = bleach.clean(  # type: ignore[no-untyped-call]
        remainder, tags=tags, attributes=attrs, strip=True
    )
    remainder_stripped = remainder_safe.strip()
    if not remainder_stripped:
        return None
    return mark_safe(remainder_stripped)


def static_image_get_with_dimensions(
    src: str,
) -> Optional[Tuple[str, int, int]]:
    """Return static image file path and dimensions."""
    cache_key = f"static_image_dimensions:{src}"
    cached_result: Optional[Tuple[str, int, int]] = cache.get(cache_key)
    if cached_result is not None:
        return cached_result

    webp_src = str(Path(src).with_suffix(".webp"))
    final_src = webp_src
    file_path = finders.find(webp_src)
    if file_path is None:
        logger.warning(".webp not found for '%s'. falling back to orig.", src)
        file_path = finders.find(src)
        final_src = src

    match file_path:
        case None:
            logger.warning("Could not find static file '%s'", src)
            return None
        case list():
            logger.warning(
                "Received multiple results for static file '%s'", src
            )
            return None
        case _:
            pass

    with Image.open(file_path) as img:
        width, height = img.size

    result = static.static(final_src), width, height
    cache.set(cache_key, result)
    return result
