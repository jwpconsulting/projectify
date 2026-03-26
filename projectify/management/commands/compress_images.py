# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2026 JWP Consulting GK
"""Compress static images to webp."""

import logging
from pathlib import Path
from typing import Any

from django.contrib.staticfiles.finders import get_finders
from django.core.management.base import BaseCommand

from PIL import Image

logger = logging.getLogger(__name__)


QUALITY = 80


class Command(BaseCommand):
    """Compress static images to webp."""

    def handle(self, *args: Any, **options: Any) -> None:
        """Execute the command."""
        del args
        del options

        # See
        # django/contrib/staticfiles/management/commands/collectstatic.py
        # Command.collect()
        static_files: list[Path] = []
        finders = get_finders()
        for finder in finders:
            for path, storage in finder.list(None):
                path = storage.path(path)
                static_files.append(Path(path))

        png_files: list[Path] = [
            p for p in static_files if p.suffix in [".png"]
        ]

        count = 0
        for count, png_path in enumerate(png_files):
            webp_path = png_path.with_suffix(".webp")
            with Image.open(png_path) as img:
                img.save(webp_path, "WebP", quality=QUALITY)
            original_size = png_path.stat().st_size
            compressed_size = webp_path.stat().st_size
            self.stdout.write(
                f"Compressed {png_path.name}. {original_size / 1024:.1f} KiB-> {compressed_size / 1024:.1f} KiB, {(original_size - compressed_size) / original_size * 100:.1f} % savings"
            )

        self.stdout.write(f"Converted {count} .png images")
