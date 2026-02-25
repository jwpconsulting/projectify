# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2026 JWP Consulting GK
"""WSGI application for Projectify."""

from configurations.wsgi import (  # type: ignore[attr-defined]
    get_wsgi_application,
)

application = get_wsgi_application()
__all__ = ("application",)
