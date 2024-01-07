# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Copyright (C) 2023 JWP Consulting GK
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""Patch classes to support generic typing."""
from collections.abc import (
    Iterable,
)
from typing import (
    Any,
)

from django.contrib import admin  # For patching
from django.views import generic  # For patching

# XXX we actually need to patch GenericAPIView
# from rest_framework import generics  # For patching
# But if we import it at this point, importing from views will read the django
# settings prematurely. Django does not care about importing views early.


patchable_classes: Iterable[Any] = (
    admin.ModelAdmin,
    admin.TabularInline,
    # XXX waiting for next version of DRF to come out with native subscription support
    # for GenericAPIView Justus 2023-07-20
    generic.View,
)


def patch() -> None:
    """Patch classes."""
    for cls in patchable_classes:
        cls.__class_getitem__ = classmethod(lambda cls, *args, **kwargs: cls)
