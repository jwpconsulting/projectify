# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2025 JWP Consulting GK

"""Form utilities."""

import logging
from typing import Any, Optional, Union

from django import forms
from django.forms import BaseForm

from rest_framework.exceptions import ValidationError

logger = logging.getLogger(__name__)


def populate_form_with_drf_errors(
    form: BaseForm, error: ValidationError
) -> None:
    """Populate a Django form with errors from a DRF ValidationError."""
    match error.detail:
        case dict():
            pass
        case _:
            logger.warning("Can't populate form %s with errors", repr(form))
            return
    for field, error_message in error.detail.items():
        # Add a non-field error to '__all__' by setting the field to None
        if field not in form.fields:
            field = None
        match error_message:
            case str():
                form.add_error(field, error_message)
            case list() as error_list:
                for e in error_list:
                    match e:
                        case str():
                            form.add_error(field, e)
                        case _:
                            logger.warning(
                                "When adding errors from a list to field %s "
                                "in form %s, found type %s "
                                "that I don't know how to handle",
                                field,
                                repr(form),
                                type(e),
                            )
            case _:
                logger.warning(
                    "When adding errors to field %s in form %s, found type %s "
                    "that I don't know how to handle",
                    field,
                    repr(form),
                    type(error_message),
                )


class SelectWOA(forms.CheckboxSelectMultiple):
    """Overwrite CheckboxSelectMultiple and pass in extra data per choice."""

    modify_choices: dict[str, dict[str, Any]]

    def __init__(
        self,
        modify_choices: dict[str, dict[str, Any]],
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Overwrite and modify choice data."""
        super().__init__(*args, **kwargs)
        self.modify_choices = modify_choices

    def create_option(
        self,
        name: str,
        value: str,
        label: Union[str, int],
        selected: Union[set[str], bool],
        index: int,
        subindex: Optional[int] = None,
        attrs: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        """Enhance options with value from modify_choices."""
        option = super().create_option(
            name, value, label, selected, index, subindex, attrs
        )
        choice = self.modify_choices[value]
        option = {**option, **choice}
        return option
