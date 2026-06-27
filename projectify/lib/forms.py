# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2025-2026 JWP Consulting GK

"""Form utilities."""

import logging
from io import BytesIO
from typing import Any, Collection, Optional, Union

from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import UploadedFile
from django.forms import BaseForm, FileField, Textarea
from django.utils.translation import gettext_lazy as _

from PIL import Image

from projectify.lib.const import RICH_TEXT_EDITOR_DEFAULT_CLASS

logger = logging.getLogger(__name__)


def populate_form_with_errors(form: BaseForm, error: ValidationError) -> None:
    """Populate a Django form with errors from a Django ValidationError."""
    if hasattr(error, "error_list") and error.error_list:
        for error in error.error_list:
            form.add_error(field=None, error=error)
    if hasattr(error, "error_dict") and error.error_dict:
        for k, errors in error.error_dict.items():
            for error in errors:
                form.add_error(k, error)


def get_image_format(file: UploadedFile) -> Optional[str]:
    """Detect image format using Pillow."""
    file.seek(0)
    image_data = BytesIO(file.read())
    file.seek(0)
    try:
        with Image.open(image_data) as img:
            return img.format
    except Exception as e:
        logger.warning(
            "Couldn't detect image format for file %s", file.name, exc_info=e
        )
    return None


# SPDX-SnippetBegin
# SPDX-License-Identifier: MIT
# SPDX-SnippetCopyrightText: 2022 LOGIC SMPC <paris@withlogic.co>
class RichTextEditor(Textarea):
    """Rich text editor widget for prose's RichTextField."""

    template_name = "common/trix-editor.html"

    def __init__(
        self,
        attrs: Optional[dict[str, Any]] = None,
        heading_blocks: bool = True,
        upload_url: Optional[str] = None,
    ):
        """Initialize the widget with optional heading_blocks and upload_url attributes."""
        existing_klass = attrs["class"] if attrs and "class" in attrs else ""
        klass = " ".join([RICH_TEXT_EDITOR_DEFAULT_CLASS, existing_klass])
        attrs = {**(attrs or {}), "class": klass}
        super().__init__(attrs)
        self.heading_blocks = heading_blocks
        self.upload_url = upload_url

    def get_context(self, name: str, value: str, attrs: Any) -> dict[str, Any]:
        """Add heading_blocks and upload_url to the context."""
        context = super().get_context(name, value, attrs)
        context["widget"] = {
            **context["widget"],
            "heading_blocks": self.heading_blocks,
            "upload_url": self.upload_url,
        }
        return context

    class Media:
        """Use vendored in trix and prose files."""

        css = {"all": ("trix/trix.css", "prose/prose.css")}
        js = ("trix/trix.umd.js", "prose/prose.js")


# TODO Consider using ImageField
class SafeImageField(FileField):
    """Image field that validates file size and type."""

    def __init__(
        self,
        *,
        allowed_file_types: Collection[str],
        allowed_file_size: int,
        **kwargs: Any,
    ):
        """Initialize with required allowed_file_types and allowed_file_size."""
        super().__init__(**kwargs)
        self.allowed_file_types = allowed_file_types
        self.allowed_file_size = allowed_file_size

    def clean(
        self, data: Any, initial: Any = None
    ) -> Union[UploadedFile, bool, None]:
        """Validate file size and type."""
        result: Union[None, UploadedFile, bool] = super().clean(data, initial)
        match result:
            case bool() | None:
                return result
            case UploadedFile() as file:
                pass
        size = file.size
        if size > self.allowed_file_size:
            raise ValidationError(
                _(
                    "Uploaded file is too large: {size} KiB. Max: {max_size} KiB"
                ).format(
                    size=size // 1024, max_size=self.allowed_file_size // 1024
                )
            )
        # Use Pillow to detect actual image format
        image_format = get_image_format(file)
        allowed = _(", ").join(list(self.allowed_file_types))
        if image_format is None:
            raise ValidationError(
                _(
                    "Upload must be one of the allowed file types: {allowed}"
                ).format(allowed=allowed)
            )
        if image_format not in self.allowed_file_types:
            raise ValidationError(
                _(
                    "{image_format} is not one of the allowed file types: {allowed}"
                ).format(image_format=image_format, allowed=allowed)
            )

        return file


# SPDX-SnippetEnd
