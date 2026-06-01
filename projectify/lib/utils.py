# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2026 JWP Consulting GK
"""Projectify utils."""

import logging
from pathlib import Path
from typing import Optional, Tuple

from django.contrib.staticfiles import finders
from django.core.cache import cache
from django.templatetags import static
from django.utils.safestring import SafeString, mark_safe

from justhtml import JustHTML, PruneEmpty
from markdown import Markdown
from PIL import Image

from projectify.lib.settings import get_settings

logger = logging.getLogger(__name__)


def clean_rich_text(unsafe_html: str) -> SafeString:
    """Clean the text for rich text content."""
    settings = get_settings()
    # https://github.com/EmilStenstrom/justhtml/blob/main/docs/sanitization.md
    sanitized_html: str = JustHTML(
        unsafe_html, policy=settings.HTML_SANITIZATION_POLICY, fragment=True
    ).to_html(pretty=False)
    # Remember that just marking it "safe" doesn't make it safe
    # sanitized_html is safe to mark as "safe" because `JustHTML` has
    # cleaned it.
    safe_html = mark_safe(sanitized_html)
    return safe_html


def extract_first_paragraph_text(unsafe_html: str) -> Optional[str]:
    """Return plain text from the first non-empty block tag in html, or None."""
    if len(unsafe_html) == 0:
        return None
    settings = get_settings()
    # Try extracting the contents of the first <p> tag
    doc = JustHTML(
        unsafe_html,
        policy=settings.HTML_SANITIZATION_POLICY,
        fragment=True,
        transforms=[PruneEmpty("*")],
    )
    if not doc.root.children:
        return None
    for child in doc.root.children:
        text: str = child.to_text()
        if len(text) > 0:
            return text
    else:
        return None


def strip_first_paragraph(unsafe_html: str) -> Optional[SafeString]:
    """
    Strip the first paragraph or other block element.

    Return all following paragraphs as long they're not empty.

    Return None if there's nothing after the first block.
    """
    if len(unsafe_html) == 0:
        return None
    settings = get_settings()
    # Try extracting the contents of the first <p> tag
    doc = JustHTML(
        unsafe_html,
        policy=settings.HTML_SANITIZATION_POLICY,
        fragment=True,
        transforms=[PruneEmpty("*")],
    )
    if not doc.root.children:
        return None
    elif len(doc.root.children) <= 1:
        return None
    else:
        doc.root.children = doc.root.children[1:]
        sanitized_html = doc.to_html()
        # calling mark_safe doesn't make it safe
        # html is safe because JustHTML outputs safe html in
        # doc.to_html()
        return mark_safe(sanitized_html)


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


def markdown_to_safe_html(
    markdown: str,
) -> tuple[SafeString, Optional[SafeString]]:
    """Convert markdown to safe html for storefront and help pages."""
    settings = get_settings()
    md = Markdown(extensions=settings.MARKDOWN_EXTENSIONS)
    unsafe_html = md.convert(markdown)
    html = clean_rich_text(unsafe_html)
    toc = getattr(md, "toc", None)
    return html, toc
