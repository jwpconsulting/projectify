# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023 JWP Consulting GK
"""Patch classes to support generic typing."""

from collections.abc import Iterable
from typing import Any

from django.contrib import admin  # For patching
from django.db import models  # For patching

patchable_classes: Iterable[Any] = (
    admin.ModelAdmin,
    admin.TabularInline,
    models.DateTimeField,
)


def patch() -> None:
    """Patch classes."""
    for cls in patchable_classes:
        cls.__class_getitem__ = classmethod(lambda cls, *args, **kwargs: cls)
