# SPDX-License-Identifier: AGPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 JWP Consulting GK
"""Projectify admin helpers."""

from typing import Optional, TypeVar

from django.db.models import Model
from django.http import HttpRequest

M = TypeVar("M", bound=Model)


class ReadOnlyAdmin[M]:
    """Admin Mixin that forbids anyone from making changes to this model."""

    def has_add_permission(
        self, request: HttpRequest, obj: Optional[M] = None
    ) -> bool:
        """Forbid anyone from adding objects."""
        del request
        del obj
        return False

    def has_change_permission(
        self, request: HttpRequest, obj: Optional[M] = None
    ) -> bool:
        """Forbid anyone from changing objects."""
        del request
        del obj
        return False

    def has_delete_permission(
        self, request: HttpRequest, obj: Optional[M] = None
    ) -> bool:
        """Forbid anyone from changing objects."""
        del request
        del obj
        return False
