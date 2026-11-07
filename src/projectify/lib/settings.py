# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2024 JWP Consulting GK
"""Settings related functions."""

from typing import cast

from django.conf import settings

from projectify.settings.base import Base


def get_settings() -> Base:
    """
    Return typed settings. Uses casting, so buyer beware.

    Still better than hoping that Django settings will contain our settings.
    """
    return cast(Base, settings)
