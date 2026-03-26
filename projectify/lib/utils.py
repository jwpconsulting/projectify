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

from PIL import Image

logger = logging.getLogger(__name__)


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
