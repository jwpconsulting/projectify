# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023 JWP Consulting GK
"""Projectify base models."""

import datetime
from collections.abc import Iterable, Sequence
from typing import Any, Callable, Optional

from django import forms
from django.db.models import CharField, DateTimeField, Model, TextField
from django.utils import safestring
from django.utils.html import strip_tags
from django.utils.translation import gettext_lazy as _

import bleach

from projectify.lib.forms import RichTextEditor
from projectify.lib.settings import get_settings

Pks = list[str]

GetOrder = Callable[[], Iterable[int]]
SetOrder = Callable[[Sequence[int]], None]


# The following code was taken from django-extensions
# SPDX-SnippetBegin
# SPDX-License-Identifier: MIT
# SPDX-SnippetCopyrightText: 2007 Michael Trier
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
        # projectify/lib/models.py:58: error: Argument 1 to "__init__" of "Field" has incompatible type "CreationDateTimeField"; expected "Field[_ST, _GT]"  [arg-type]
        DateTimeField[datetime.datetime].__init__(self, *args, **kwargs)

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
        # projectify/lib/models.py:88: error: Argument 1 to "__init__" of "Field" has incompatible type "ModificationDateTimeField"; expected "Field[_ST, _GT]"  [arg-type]
        DateTimeField[datetime.datetime].__init__(self, *args, **kwargs)

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


class TitleDescriptionModel(Model):
    """
    TitleDescriptionModel from django-extensions.

    An abstract base class model that provides title and description fields.
    """

    title = CharField(_("title"), max_length=255)
    description = TextField(_("description"), blank=True, null=True)

    class Meta:
        """Meta."""

        abstract = True


# SPDX-SnippetEnd


class BaseModel(Model):
    """
    The base model to use for all Projectify models.

    This previously used the django-extensions TimeStampedModel. Since only the
    created and modified fields were needed, they were copied here and the save
    override was left out.
    """

    created = CreationDateTimeField(verbose_name=_("created"))
    modified = ModificationDateTimeField(verbose_name=_("modified"))
    # TODO add full_clean() on save()

    class Meta:
        """Make this model abstract."""

        abstract = True
        get_latest_by = "modified"


# SPDX-SnippetBegin
# SPDX-License-Identifier: MIT
# SPDX-SnippetCopyrightText: 2022 LOGIC SMPC <paris@withlogic.co>
def clean_rich_text(text: str) -> safestring.SafeString:
    """Clean the text for rich text content."""
    settings = get_settings()
    tags = settings.MARKDOWNIFY["default"]["WHITELIST_TAGS"]
    attrs = settings.MARKDOWNIFY["default"]["WHITELIST_ATTRS"]
    sanitized_html: str = bleach.clean(text, tags=tags, attributes=attrs)  # type: ignore[no-untyped-call]
    # Remember that just marking it "safe" doesn't make it safe
    # sanitized_html is safe to mark as "safe" because `bleach.clean` has
    # cleaned it.
    safe_html = safestring.mark_safe(sanitized_html)
    return safe_html


class RichTextField(TextField):  # type: ignore
    """Vendored in RichTextField from django-prose."""

    def formfield(self, **kwargs: Any) -> forms.Field:
        """Return widget."""
        kwargs = {**kwargs, "widget": RichTextEditor}
        field: forms.Field = super().formfield(**kwargs)
        return field

    def pre_save(self, model_instance: Model, add: bool) -> str:
        """Pre save."""
        del add
        raw_html: str = getattr(model_instance, self.attname)
        if not raw_html:
            return raw_html

        sanitized_html = clean_rich_text(raw_html)
        return sanitized_html

    def from_db_value(
        self, value: Optional[str], expression: object, connection: object
    ) -> Optional[safestring.SafeString]:
        """Return sanitized value."""
        if value is None:
            return value
        sanitized_html = clean_rich_text(value)
        return sanitized_html


class DocumentContentField(RichTextField):
    """Class copied in from prose/fields.py."""


class AbstractDocument(Model):
    """Class copied in from prose/models.py."""

    content = DocumentContentField()

    def get_plain_text_content(self) -> str:
        """Return plain text content."""
        return strip_tags(self.content)

    def __str__(self) -> str:
        """Return string representation."""
        plain_text = self.get_plain_text_content()

        if len(plain_text) < 32:
            return plain_text

        return f"{plain_text[:28]}..."

    class Meta:
        """Make this an abstract class."""

        abstract = True


# SPDX-SnippetEnd
