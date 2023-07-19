"""Patch classes to support generic typing."""
from collections.abc import (
    Iterable,
)
from typing import (
    Any,
)

from django.contrib import admin  # For patching
from django.views import generic  # For patching

from factory import django  # For patching


# XXX we actually need to patch GenericAPIView
# from rest_framework import generics  # For patching
# But if we import it at this point, importing from views will read the django
# settings prematurely. Django does not care about importing views early.


patchable_classes: Iterable[Any] = (
    admin.ModelAdmin,
    admin.TabularInline,
    django.DjangoModelFactory,
    # XXX waiting for next version of DRF to come out with native subscription support
    # for GenericAPIView Justus 2023-07-20
    generic.View,
)


def patch() -> None:
    """Patch classes."""
    for cls in patchable_classes:
        cls.__class_getitem__ = classmethod(lambda cls, *args, **kwargs: cls)
