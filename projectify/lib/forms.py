# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2025-2026 JWP Consulting GK

"""Form utilities."""

import logging

from django.core.exceptions import ValidationError
from django.forms import BaseForm

logger = logging.getLogger(__name__)


def populate_form_with_drf_errors(
    form: BaseForm, error: ValidationError
) -> None:
    """Populate a Django form with errors from a Django ValidationError."""
    if hasattr(error, "error_list") and error.error_list:
        for error in error.error_list:
            form.add_error(field=None, error=error)
    if hasattr(error, "error_dict") and error.error_dict:
        for k, errors in error.error_dict.items():
            for error in errors:
                form.add_error(k, error)
    return
