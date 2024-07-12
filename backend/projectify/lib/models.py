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
"""Projectify base models."""

import datetime
from typing import Any

from django.db.models import DateTimeField, Model
from django.utils.translation import gettext_lazy as _

# The following code was taken from django-extensions
# Copyright (c) 2007 Michael Trier


# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
class CreationDateTimeField(DateTimeField[datetime.datetime]):
    """
    CreationDateTimeField from django-extensions.

    By default, sets editable=False, blank=True, auto_now_add=True
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Override constructor."""
        kwargs.setdefault("editable", False)
        kwargs.setdefault("blank", True)
        kwargs.setdefault("auto_now_add", True)
        super().__init__(*args, **kwargs)

    def get_internal_type(self) -> str:
        """Return internal type."""
        return "DateTimeField"

    def deconstruct(self) -> tuple[Any, Any, Any, Any]:
        """Return enough information to construct CreationDateTimeField."""
        name, path, args, kwargs = super().deconstruct()
        if self.editable is not False:
            kwargs["editable"] = True
        if self.blank is not True:
            kwargs["blank"] = False
        if self.auto_now_add is not False:
            kwargs["auto_now_add"] = True
        return name, path, args, kwargs


class ModificationDateTimeField(CreationDateTimeField):
    """
    ModificationDateTimeField from django-extensions.

    By default, sets editable=False, blank=True, auto_now=True

    Sets value to now every time the object is saved.
    """

    def __init__(self, *args: Any, **kwargs: Any):
        """Enable auto_now=True."""
        kwargs.setdefault("auto_now", True)
        super().__init__(*args, **kwargs)

    def get_internal_type(self) -> str:
        """Return internal type."""
        return "DateTimeField"

    def deconstruct(self) -> tuple[Any, Any, Any, Any]:
        """Return enough information to construct ModificationDateTimeField."""
        name, path, args, kwargs = super().deconstruct()
        if self.auto_now is not False:
            kwargs["auto_now"] = True
        return name, path, args, kwargs

    def pre_save(self, model_instance: Model, add: bool) -> Any:
        """Update the time stamp."""
        if not getattr(model_instance, "update_modified", True):
            return getattr(model_instance, self.attname)
        return super().pre_save(model_instance, add)


class BaseModel(Model):
    """
    The base model to use for all Projectify models.

    This previously used the django-extensions TimeStampedModel. Since only the
    created and modified fields were needed, they were copied here and the save
    override was left out.
    """

    created = CreationDateTimeField(verbose_name=_("created"))
    modified = ModificationDateTimeField(verbose_name=_("modified"))

    class Meta:
        """Make this model abstract."""

        abstract = True
        get_latest_by = "modified"
