# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2025-2026 JWP Consulting GK

"""Form utilities."""

import logging
from typing import Any

from django.core.exceptions import ValidationError
from django.forms import BaseForm, Textarea

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


# SPDX-SnippetBegin
# SPDX-License-Identifier: MIT
# SPDX-SnippetCopyrightText: 2022 LOGIC SMPC <paris@withlogic.co>
class RichTextEditor(Textarea):
    """Rich text editor widget for prose's RichTextField."""

    template_name = "prose/forms/widgets/editor.html"

    def __init__(self, attrs: Any = None, heading_blocks: bool = True):
        """Initialize the widget with optional heading_blocks attribute."""
        super().__init__(attrs)
        self.heading_blocks = heading_blocks

    def get_context(self, name: str, value: str, attrs: Any):
        """Add heading_blocks to the context."""
        context = super().get_context(name, value, attrs)
        context["widget"]["heading_blocks"] = self.heading_blocks
        return context

    class Media:
        """Use vendored in {trix,prose}.{css,js}."""

        css = {"all": ("trix/trix.css", "trix/prose.css")}
        js = ("trix/trix.js", "trix/prose.js")


# SPDX-SnippetEnd
