"""Patch classes to support generic typing."""
from collections.abc import (
    Iterable,
)
from typing import (
    Any,
)

from django.contrib import admin  # For patching

from factory import django  # For patching


patchable_classes: Iterable[Any] = (
    admin.ModelAdmin,
    admin.TabularInline,
    django.DjangoModelFactory,
)


def patch() -> None:
    """Patch classes."""
    for cls in patchable_classes:
        cls.__class_getitem__ = classmethod(lambda cls, *args, **kwargs: cls)
