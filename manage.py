#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import sys
from os import (
    environ,
)

from dotenv import (
    load_dotenv,
)

load_dotenv()


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
        from configurations.management import (
            execute_from_command_line,
        )
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
