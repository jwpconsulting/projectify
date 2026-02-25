#!/usr/bin/env python
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2021, 2023, 2024 JWP Consulting GK
"""Django's command-line utility for administrative tasks."""

import sys
import warnings
from os import environ

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    warnings.warn("Starting ./manage.py without dotenv.load_dotenv()")


def main() -> None:
    """Run administrative tasks."""
    if "DJANGO_SETTINGS_MODULE" not in environ:
        raise ValueError(
            "You must specify the environment variable "
            "DJANGO_SETTINGS_MODULE. Please verify whether this variable is "
            "present in your .env file or environment"
        )
    if "DJANGO_CONFIGURATION" not in environ:
        raise ValueError(
            "You must specify the django-configurations specific "
            "environment variable DJANGO_CONFIGURATION. Please verify "
            "whether this variable is present in your .env file or "
            "environment. See the projectify/settings folder for all "
            "available configuration classes."
        )
    try:
        from configurations.management import (  # type: ignore[attr-defined]
            execute_from_command_line,
        )
    except ImportError as exc:
        raise ImportError(
            "Couldn't import configurations. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate your virtual environment?"
        ) from exc

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
