# SPDX-FileCopyrightText: 2024 JWP Consulting GK
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from django.core.handlers.asgi import (
    ASGIHandler,
)

def get_asgi_application() -> ASGIHandler: ...
