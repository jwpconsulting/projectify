# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2024 JWP Consulting GK
"""View decorators."""

from typing import Any, Callable

from django.contrib.auth.decorators import login_required


def platform_view(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    Wrap view in login_required.

    This makes it easier to add required decorators or other things to views
    that are part of the platform, i.e., pages that require the user to be
    logged in.
    """
    return login_required(func)
