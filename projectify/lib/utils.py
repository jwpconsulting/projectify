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

from justhtml import JustHTML, SanitizationPolicy
from markdown import Markdown
from PIL import Image

from projectify.lib.settings import get_settings

logger = logging.getLogger(__name__)


settings = get_settings()


def clean_rich_text(
    unsafe_html: str, policy: SanitizationPolicy = settings.HTML_USER_POLICY
) -> SafeString:
    """Clean the text for rich text content."""
    # https://github.com/EmilStenstrom/justhtml/blob/main/docs/sanitization.md
    sanitized_html: str = JustHTML(
        unsafe_html, policy=policy, fragment=True
    ).to_html(pretty=False)
    # Remember that just marking it "safe" doesn't make it safe
    # sanitized_html is safe to mark as "safe" because `JustHTML` has
    # cleaned it.
    safe_html = mark_safe(sanitized_html)
    return safe_html


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
    sanitized_html: str = JustHTML(
        # NOTE: This uses the HTML_PROJECTIFY_POLICY and is only
        # suitable for content coming from Projectify
        unsafe_html,
        policy=settings.HTML_PROJECTIFY_POLICY,
        fragment=True,
        strict=True,
    ).to_html(pretty=False)
    safe_html = mark_safe(sanitized_html)
    unsafe_toc_html = getattr(md, "toc", None)
    if unsafe_toc_html:
        sanitzed_toc_html = JustHTML(
            unsafe_toc_html,
            policy=settings.HTML_PROJECTIFY_POLICY,
            fragment=True,
            strict=True,
        ).to_html(pretty=False)
        safe_toc = mark_safe(sanitzed_toc_html)
    else:
        safe_toc = None
    return safe_html, safe_toc
