# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2026 JWP Consulting GK
"""Management command to generate favicon files from SVG."""

import io
import subprocess
from pathlib import Path
from typing import Any

from django.contrib.staticfiles import finders
from django.core.management.base import BaseCommand, CommandError

from PIL import Image

SOURCE_FILE = "favicon.svg"


class Command(BaseCommand):
    """Generate favicon.ico and apple-touch-icon.png from favicon.svg."""

    help = "Generate favicon.ico and apple-touch-icon.png from favicon.svg"

    def handle(self, *args: Any, **options: Any) -> None:
        """Handle the command."""
        del args, options

        match finders.find(SOURCE_FILE):
            case str() as source_path_str:
                source_path = Path(source_path_str)
            case list() as list_of_paths:
                raise RuntimeError(
                    f"Expected string, got list {list_of_paths}"
                )
            case None:
                raise CommandError(
                    f"Source file {SOURCE_FILE} not found in static files"
                )
        favicon_ico_path = source_path.parent / "favicon.ico"
        apple_touch_icon_path = source_path.parent / "apple-touch-icon.png"

        png_data = subprocess.run(
            [
                "rsvg-convert",
                "--width",
                "32",
                "--height",
                "32",
                "--format",
                "png",
                str(source_path),
            ],
            check=True,
            stdout=subprocess.PIPE,
        ).stdout

        with Image.open(io.BytesIO(png_data)) as img:
            img.save(favicon_ico_path, format="ICO", sizes=[(32, 32)])

        self.stdout.write(f"Created {favicon_ico_path}", self.style.SUCCESS)

        subprocess.run(
            [
                "rsvg-convert",
                "--width",
                "180",
                "--height",
                "180",
                "--format",
                "png",
                "--output",
                str(apple_touch_icon_path),
                str(source_path),
            ],
            check=True,
        )

        self.stdout.write(
            f"Created {apple_touch_icon_path}", self.style.SUCCESS
        )
