# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2021, 2022, 2023 JWP Consulting GK
"""
ASGI config for projectify project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from configurations.asgi import (  # type: ignore[attr-defined]
    get_asgi_application,
)

# TODO still needed? We should just let the server crash when this env var is
# unset
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", "projectify.settings.production"
)

application = get_asgi_application()
__all__ = ("application",)
